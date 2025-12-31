#!/usr/bin/env python3
"""
OnHockey.tv Game Schedule Scraper

Fetches and parses the live hockey game schedule from onhockey.tv,
extracting game times, teams, leagues, and available stream links.

Author: Claude
License: MIT
"""

import re
import json
import argparse
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, field, asdict
from typing import Optional
from html.parser import HTMLParser
import urllib.request
import urllib.error


@dataclass
class StreamLink:
    """Represents a single stream link for a game."""
    url: str
    source: str  # e.g., 'streamd', 'freestr', 'ddlive'
    channel: Optional[str] = None  # e.g., 'TSN 5', 'NHL Network'
    feed_type: str = "main"  # 'home', 'away', 'main', or language like 'russian', 'french'


@dataclass
class Game:
    """Represents a single hockey game."""
    league: str
    league_icon: Optional[str]
    home_team: str
    away_team: str
    time_gmt: str  # Original GMT time from the site
    time_local: Optional[str] = None  # Converted to local timezone
    streams: list[StreamLink] = field(default_factory=list)
    standings_url: Optional[str] = None
    is_live: bool = False
    stream_count: int = 0

    def __post_init__(self):
        self.stream_count = len(self.streams)


class ScheduleParser(HTMLParser):
    """Parses the schedule_table.php HTML response."""
    
    def __init__(self, timezone_offset: int = -7):
        super().__init__()
        self.games: list[Game] = []
        self.current_league: str = ""
        self.current_league_icon: Optional[str] = None
        self.current_standings_url: Optional[str] = None
        self.timezone_offset = timezone_offset
        
        # Parser state
        self.in_game_row = False
        self.in_game_cell = False
        self.in_time_cell = False
        self.in_league_row = False
        self.in_gamelinks = False
        self.current_feed_type = "main"
        
        self.current_game_time = ""
        self.current_game_text = ""
        self.current_streams: list[StreamLink] = []
        self.current_link_buffer = ""
        
    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]):
        attrs_dict = dict(attrs)
        
        # Detect league header row
        if tag == "tr" and attrs_dict.get("bgcolor") == "#3z3z3z":
            self.in_league_row = True
            
        # Detect league icon
        if tag == "td" and self.in_league_row:
            bg = attrs_dict.get("background", "")
            if "ico" in bg:
                self.current_league_icon = bg
                
        # Detect standings link
        if tag == "a" and self.in_league_row:
            href = attrs_dict.get("href", "")
            if "standings.php" in href:
                self.current_standings_url = f"https://onhockey.tv/{href}"
        
        # Detect game row
        if tag == "tr" and attrs_dict.get("class") == "game":
            self.in_game_row = True
            self.current_game_time = ""
            self.current_game_text = ""
            self.current_streams = []
            
        # Time cell (contains <text class='game_hour'>)
        if tag == "text" and attrs_dict.get("class") == "game_hour":
            self.in_time_cell = True
            
        # Game info cell (second td in game row)
        if tag == "td" and self.in_game_row and not self.in_time_cell:
            self.in_game_cell = True
            
        # Gamelinks div
        if tag == "div" and attrs_dict.get("class") == "gamelinks":
            self.in_gamelinks = True
            
        # Stream links
        if tag == "a" and self.in_gamelinks:
            href = attrs_dict.get("href", "")
            title = attrs_dict.get("title", "")
            
            # Extract the actual stream URL from the wrapper
            if "channel=" in href:
                match = re.search(r'channel=([^&\s]+)', href)
                if match:
                    stream_url = match.group(1)
                    # Clean up URL
                    if stream_url.startswith("//"):
                        stream_url = "https:" + stream_url
                    self.current_link_buffer = stream_url
            elif href.startswith("//"):
                self.current_link_buffer = "https:" + href
            else:
                self.current_link_buffer = href
                
            # We'll get the source name from the link text in handle_data
            
    def handle_endtag(self, tag: str):
        if tag == "tr":
            if self.in_league_row:
                self.in_league_row = False
            elif self.in_game_row:
                # Finalize game
                self._finalize_game()
                self.in_game_row = False
                
        if tag == "td":
            self.in_game_cell = False
            self.in_time_cell = False
            
        if tag == "div" and self.in_gamelinks:
            self.in_gamelinks = False
            
        if tag == "a" and self.current_link_buffer:
            self.current_link_buffer = ""
            
    def handle_data(self, data: str):
        data = data.strip()
        if not data:
            return
            
        # League name (bold text in league row)
        if self.in_league_row and data and not data.startswith("standings"):
            if data not in ("", "standings"):
                self.current_league = data
                
        # Time hour
        if self.in_time_cell:
            self.current_game_time = data
            
        # Time minutes (after the hour, outside the <text> tag)
        if self.in_game_row and not self.in_game_cell and not self.in_time_cell:
            if data.startswith(":"):
                self.current_game_time += data
                
        # Game teams
        if self.in_game_cell and not self.in_gamelinks:
            if " - " in data:
                self.current_game_text = data
                
        # Feed type markers
        if self.in_gamelinks:
            lower_data = data.lower()
            if lower_data.endswith(":") or lower_data.endswith(" feed:"):
                if "home" in lower_data:
                    self.current_feed_type = "home"
                elif "away" in lower_data:
                    self.current_feed_type = "away"
                elif "russian" in lower_data:
                    self.current_feed_type = "russian"
                elif "czech" in lower_data:
                    self.current_feed_type = "czech"
                elif "french" in lower_data:
                    self.current_feed_type = "french"
                elif "swedish" in lower_data:
                    self.current_feed_type = "swedish"
                elif "english" in lower_data:
                    self.current_feed_type = "english"
                else:
                    self.current_feed_type = "main"
                    
            # Stream source name (link text like 'streamd', 'freestr', etc.)
            if self.current_link_buffer and data:
                # Get the title from the most recent link if we stored it
                stream = StreamLink(
                    url=self.current_link_buffer,
                    source=data,
                    feed_type=self.current_feed_type
                )
                self.current_streams.append(stream)
                self.current_link_buffer = ""
                
    def _finalize_game(self):
        """Create a Game object from the current parsed data."""
        if not self.current_game_text or " - " not in self.current_game_text:
            return
            
        teams = self.current_game_text.split(" - ", 1)
        if len(teams) != 2:
            return
            
        home_team, away_team = teams[0].strip(), teams[1].strip()
        
        # Convert time to local
        local_time = self._convert_time(self.current_game_time)
        
        game = Game(
            league=self.current_league,
            league_icon=self.current_league_icon,
            home_team=home_team,
            away_team=away_team,
            time_gmt=self.current_game_time,
            time_local=local_time,
            streams=self.current_streams.copy(),
            standings_url=self.current_standings_url,
            is_live=len(self.current_streams) > 0
        )
        self.games.append(game)
        self.current_feed_type = "main"
        
    def _convert_time(self, gmt_time: str) -> str:
        """Convert GMT time string to local time."""
        try:
            # Parse hour:minute
            parts = gmt_time.split(":")
            if len(parts) != 2:
                return gmt_time
            hour, minute = int(parts[0]), int(parts[1])
            
            # Apply timezone offset
            hour += self.timezone_offset
            
            # Handle day wraparound
            day_offset = ""
            if hour < 0:
                hour += 24
                day_offset = " (yesterday)"
            elif hour >= 24:
                hour -= 24
                day_offset = " (tomorrow)"
                
            return f"{hour:02d}:{minute:02d}{day_offset}"
        except (ValueError, IndexError):
            return gmt_time


def fetch_schedule(timezone_offset: int = -7) -> list[Game]:
    """
    Fetch and parse the game schedule from onhockey.tv.
    
    Args:
        timezone_offset: Hours offset from GMT (e.g., -7 for MST)
        
    Returns:
        List of Game objects
    """
    url = "https://onhockey.tv/schedule_table.php"
    headers = {
        "Referer": "https://onhockey.tv/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as e:
        print(f"Error fetching schedule: {e}")
        return []
        
    parser = ScheduleParser(timezone_offset=timezone_offset)
    parser.feed(html)
    
    return parser.games


def print_schedule(games: list[Game], show_streams: bool = True, 
                   league_filter: Optional[str] = None,
                   json_output: bool = False):
    """
    Print the game schedule in a readable format.
    
    Args:
        games: List of Game objects
        show_streams: Whether to show stream links
        league_filter: Filter to specific league (case-insensitive)
        json_output: Output as JSON instead of formatted text
    """
    if league_filter:
        games = [g for g in games if league_filter.lower() in g.league.lower()]
        
    if json_output:
        output = [asdict(g) for g in games]
        print(json.dumps(output, indent=2))
        return
        
    if not games:
        print("No games found.")
        return
        
    current_league = ""
    
    for game in games:
        # Print league header
        if game.league != current_league:
            current_league = game.league
            print(f"\n{'='*60}")
            print(f"  {current_league}")
            if game.standings_url:
                print(f"  Standings: {game.standings_url}")
            print(f"{'='*60}")
            
        # Print game info
        status = "🔴 LIVE" if game.streams else "⏰ Upcoming"
        print(f"\n{game.time_local} (GMT {game.time_gmt})  {status}")
        print(f"  {game.home_team}  vs  {game.away_team}")
        
        if show_streams and game.streams:
            print(f"  Streams ({len(game.streams)} available):")
            
            # Group by feed type
            feeds: dict[str, list[StreamLink]] = {}
            for stream in game.streams:
                if stream.feed_type not in feeds:
                    feeds[stream.feed_type] = []
                feeds[stream.feed_type].append(stream)
                
            for feed_type, streams in feeds.items():
                print(f"    [{feed_type}]")
                for s in streams[:5]:  # Limit to 5 per feed type
                    channel_info = f" ({s.channel})" if s.channel else ""
                    print(f"      • {s.source}{channel_info}: {s.url}")
                if len(streams) > 5:
                    print(f"      ... and {len(streams) - 5} more")
        elif not game.streams:
            print("  Streams: Available closer to game time")
            

def get_stream_urls(games: list[Game], team_filter: Optional[str] = None) -> list[str]:
    """
    Extract direct stream URLs for testing or playback.
    
    Args:
        games: List of Game objects
        team_filter: Filter to games involving this team (case-insensitive)
        
    Returns:
        List of stream URLs
    """
    urls = []
    
    for game in games:
        if team_filter:
            team_lower = team_filter.lower()
            if team_lower not in game.home_team.lower() and team_lower not in game.away_team.lower():
                continue
                
        for stream in game.streams:
            if stream.url and stream.url.startswith("http"):
                urls.append(stream.url)
                
    return urls


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and display hockey game schedules from OnHockey.tv"
    )
    parser.add_argument(
        "-t", "--timezone", 
        type=int, 
        default=-7,
        help="Timezone offset from GMT (default: -7 for MST)"
    )
    parser.add_argument(
        "-l", "--league",
        type=str,
        help="Filter by league name (e.g., 'NHL', 'World Junior')"
    )
    parser.add_argument(
        "--team",
        type=str,
        help="Filter by team name"
    )
    parser.add_argument(
        "--no-streams",
        action="store_true",
        help="Hide stream links"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--urls-only",
        action="store_true",
        help="Output only stream URLs (one per line)"
    )
    
    args = parser.parse_args()
    
    print("Fetching schedule from onhockey.tv...")
    games = fetch_schedule(timezone_offset=args.timezone)
    
    if not games:
        print("Failed to fetch schedule or no games found.")
        return
        
    print(f"Found {len(games)} games.\n")
    
    if args.urls_only:
        urls = get_stream_urls(games, team_filter=args.team)
        for url in urls:
            print(url)
    else:
        print_schedule(
            games,
            show_streams=not args.no_streams,
            league_filter=args.league,
            json_output=args.json
        )


if __name__ == "__main__":
    main()