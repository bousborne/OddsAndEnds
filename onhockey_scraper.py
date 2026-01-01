#!/usr/bin/env python3
"""
OnHockey.tv Game Schedule Scraper

Fetches and parses the live hockey game schedule from onhockey.tv,
extracting game times, teams, leagues, and available stream links.
Attempts to extract actual m3u8 stream URLs using multiple methods.

Author: Claude
License: MIT
"""

import re
import json
import argparse
import base64
import subprocess
import shutil
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, field, asdict
from typing import Optional
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request
import urllib.error


@dataclass
class StreamLink:
    """Represents a single stream link for a game."""
    url: str
    source: str  # e.g., 'streamd', 'freestr', 'ddlive'
    channel: Optional[str] = None  # e.g., 'TSN 5', 'NHL Network'
    feed_type: str = "main"  # 'home', 'away', 'main', or language like 'russian', 'french'
    m3u8_url: Optional[str] = None  # Extracted direct stream URL
    verified: bool = False  # Whether the stream was verified working
    extraction_method: Optional[str] = None  # How we found the m3u8


class StreamExtractor:
    """Extracts actual m3u8 stream URLs from embed pages using multiple methods."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.has_ytdlp = shutil.which("yt-dlp") is not None
        self.has_curl = shutil.which("curl") is not None
        
    def log(self, msg: str):
        if self.verbose:
            print(f"  [extractor] {msg}")
            
    def extract(self, embed_url: str, referer: str = "https://onhockey.tv/") -> Optional[tuple[str, str]]:
        """
        Try multiple methods to extract m3u8 URL from an embed page.
        
        Returns:
            Tuple of (m3u8_url, method_used) or None if extraction failed
        """
        # Method 1: Check for base64-encoded paths in HTML (wikisport style)
        result = self._try_base64_extraction(embed_url, referer)
        if result:
            return result
            
        # Method 2: Look for direct m3u8 references in HTML
        result = self._try_direct_m3u8_scan(embed_url, referer)
        if result:
            return result
            
        # Method 3: Try yt-dlp (handles JS-based players)
        if self.has_ytdlp:
            result = self._try_ytdlp(embed_url, referer)
            if result:
                return result
                
        return None
        
    def _fetch_page(self, url: str, referer: str) -> Optional[str]:
        """Fetch a page with proper headers."""
        try:
            if self.has_curl:
                result = subprocess.run(
                    ["curl", "-s", "-H", f"Referer: {referer}", 
                     "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                     "--max-time", "10", url],
                    capture_output=True, text=True, timeout=15
                )
                if result.returncode == 0:
                    return result.stdout
            else:
                req = urllib.request.Request(url, headers={
                    "Referer": referer,
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                })
                with urllib.request.urlopen(req, timeout=10) as resp:
                    return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            self.log(f"Fetch failed for {url}: {e}")
        return None
        
    def _try_base64_extraction(self, url: str, referer: str) -> Optional[tuple[str, str]]:
        """Look for base64-encoded stream paths in the page."""
        self.log(f"Trying base64 extraction on {url}")
        
        html = self._fetch_page(url, referer)
        if not html:
            return None
            
        # Look for atob('...') patterns
        atob_pattern = r"atob\(['\"]([A-Za-z0-9+/=]+)['\"]\)"
        matches = re.findall(atob_pattern, html)
        
        for match in matches:
            try:
                decoded = base64.b64decode(match).decode("utf-8")
                self.log(f"Decoded base64: {decoded}")
                
                # Check if it looks like an m3u8 path
                if ".m3u8" in decoded or "/hls/" in decoded or "/stream" in decoded:
                    # Build full URL
                    from urllib.parse import urlparse, urljoin
                    parsed = urlparse(url)
                    base = f"{parsed.scheme}://{parsed.netloc}"
                    
                    if decoded.startswith("/"):
                        m3u8_url = base + decoded
                    elif decoded.startswith("http"):
                        m3u8_url = decoded
                    else:
                        m3u8_url = urljoin(url, decoded)
                        
                    return (m3u8_url, "base64")
            except Exception as e:
                self.log(f"Base64 decode failed: {e}")
                continue
                
        return None
        
    def _try_direct_m3u8_scan(self, url: str, referer: str) -> Optional[tuple[str, str]]:
        """Scan HTML for direct m3u8 URLs."""
        self.log(f"Scanning for direct m3u8 in {url}")
        
        html = self._fetch_page(url, referer)
        if not html:
            return None
            
        # Look for m3u8 URLs directly in the HTML
        m3u8_patterns = [
            r'(https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*)',
            r'["\']([^"\']*\.m3u8[^"\']*)["\']',
            r'src[=:]\s*["\']?(https?://[^\s"\'<>]+)["\']?',
        ]
        
        for pattern in m3u8_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if ".m3u8" in match and "http" in match:
                    self.log(f"Found direct m3u8: {match}")
                    return (match, "direct_scan")
                    
        # Look for kinescope/fluidplayer URLs (Russian streams)
        kinescope_pattern = r'(https?://[^\s"\'<>]*kinescope[^\s"\'<>]*master\.m3u8[^\s"\'<>]*)'
        matches = re.findall(kinescope_pattern, html, re.IGNORECASE)
        if matches:
            return (matches[0], "kinescope")
            
        return None
        
    def _try_ytdlp(self, url: str, referer: str) -> Optional[tuple[str, str]]:
        """Use yt-dlp to extract stream URL."""
        self.log(f"Trying yt-dlp on {url}")
        
        try:
            result = subprocess.run(
                ["yt-dlp", "--referer", referer, "-g", "--no-warnings", url],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0 and result.stdout.strip():
                stream_url = result.stdout.strip().split("\n")[0]
                if stream_url.startswith("http"):
                    self.log(f"yt-dlp found: {stream_url}")
                    return (stream_url, "yt-dlp")
        except subprocess.TimeoutExpired:
            self.log("yt-dlp timed out")
        except Exception as e:
            self.log(f"yt-dlp failed: {e}")
            
        return None


class StreamVerifier:
    """Verifies that extracted streams are actually working."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.has_curl = shutil.which("curl") is not None
        self.has_ffprobe = shutil.which("ffprobe") is not None
        
    def log(self, msg: str):
        if self.verbose:
            print(f"  [verifier] {msg}")
            
    def verify(self, m3u8_url: str, referer: str = None) -> tuple[bool, Optional[dict]]:
        """
        Verify a stream URL is working and get basic info.
        
        Returns:
            Tuple of (is_working, info_dict)
        """
        # First try a simple HEAD/GET request to check if URL responds
        if not self._check_url_responds(m3u8_url, referer):
            return (False, None)
            
        # Check if it's actually an m3u8 playlist
        content = self._fetch_content(m3u8_url, referer)
        if not content:
            return (False, None)
            
        if "#EXTM3U" not in content and "#EXT-X-" not in content:
            self.log("Not a valid m3u8 playlist")
            return (False, None)
            
        # Parse some basic info from the playlist
        info = self._parse_m3u8_info(content, m3u8_url)
        
        # Optionally use ffprobe for more detailed verification
        if self.has_ffprobe:
            probe_info = self._ffprobe_check(m3u8_url, referer)
            if probe_info:
                info.update(probe_info)
                
        return (True, info)
        
    def _check_url_responds(self, url: str, referer: str = None) -> bool:
        """Quick check if URL responds at all."""
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            if referer:
                headers["Referer"] = referer
                
            if self.has_curl:
                cmd = ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", 
                       "--max-time", "5", "-H", f"User-Agent: {headers['User-Agent']}"]
                if referer:
                    cmd.extend(["-H", f"Referer: {referer}"])
                cmd.append(url)
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                status = result.stdout.strip()
                self.log(f"URL status: {status}")
                return status.startswith("2") or status.startswith("3")
            else:
                req = urllib.request.Request(url, headers=headers, method="HEAD")
                with urllib.request.urlopen(req, timeout=5) as resp:
                    return resp.status < 400
        except Exception as e:
            self.log(f"URL check failed: {e}")
            return False
            
    def _fetch_content(self, url: str, referer: str = None) -> Optional[str]:
        """Fetch the m3u8 content."""
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            if referer:
                headers["Referer"] = referer
                
            if self.has_curl:
                cmd = ["curl", "-s", "--max-time", "10",
                       "-H", f"User-Agent: {headers['User-Agent']}"]
                if referer:
                    cmd.extend(["-H", f"Referer: {referer}"])
                cmd.append(url)
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                if result.returncode == 0:
                    return result.stdout
            else:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as resp:
                    return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            self.log(f"Content fetch failed: {e}")
        return None
        
    def _parse_m3u8_info(self, content: str, url: str) -> dict:
        """Parse basic info from m3u8 playlist."""
        info = {"type": "unknown", "variants": []}
        
        # Check if master playlist (has stream variants)
        if "#EXT-X-STREAM-INF" in content:
            info["type"] = "master"
            # Extract resolutions/bandwidths
            for match in re.finditer(r'#EXT-X-STREAM-INF:([^\n]+)', content):
                variant_info = match.group(1)
                variant = {}
                
                res_match = re.search(r'RESOLUTION=(\d+x\d+)', variant_info)
                if res_match:
                    variant["resolution"] = res_match.group(1)
                    
                bw_match = re.search(r'BANDWIDTH=(\d+)', variant_info)
                if bw_match:
                    variant["bandwidth_kbps"] = int(bw_match.group(1)) // 1000
                    
                if variant:
                    info["variants"].append(variant)
        else:
            info["type"] = "media"
            
        # Check for live vs VOD
        if "#EXT-X-ENDLIST" in content:
            info["live"] = False
        else:
            info["live"] = True
            
        return info
        
    def _ffprobe_check(self, url: str, referer: str = None) -> Optional[dict]:
        """Use ffprobe for detailed stream verification."""
        try:
            cmd = ["ffprobe", "-v", "quiet", "-print_format", "json",
                   "-show_format", "-show_streams", "-analyzeduration", "2000000"]
            
            if referer:
                cmd.extend(["-headers", f"Referer: {referer}\r\n"])
                
            cmd.append(url)
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                info = {}
                
                if "format" in data:
                    info["format"] = data["format"].get("format_name")
                    
                if "streams" in data:
                    for stream in data["streams"]:
                        if stream.get("codec_type") == "video":
                            info["video_codec"] = stream.get("codec_name")
                            info["width"] = stream.get("width")
                            info["height"] = stream.get("height")
                        elif stream.get("codec_type") == "audio":
                            info["audio_codec"] = stream.get("codec_name")
                            
                return info if info else None
        except Exception as e:
            self.log(f"ffprobe failed: {e}")
        return None


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
                   json_output: bool = False,
                   verified_only: bool = False):
    """
    Print the game schedule in a readable format.
    
    Args:
        games: List of Game objects
        show_streams: Whether to show stream links
        league_filter: Filter to specific league (case-insensitive)
        json_output: Output as JSON instead of formatted text
        verified_only: Only show verified working streams
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
            print(f"\n{'='*70}")
            print(f"  {current_league}")
            if game.standings_url:
                print(f"  Standings: {game.standings_url}")
            print(f"{'='*70}")
            
        # Print game info
        status = "🔴 LIVE" if game.streams else "⏰ Upcoming"
        print(f"\n{game.time_local} (GMT {game.time_gmt})  {status}")
        print(f"  {game.home_team}  vs  {game.away_team}")
        
        if show_streams and game.streams:
            # Count verified streams
            verified_streams = [s for s in game.streams if s.verified]
            total_streams = len(game.streams)
            
            print(f"  Streams: {len(verified_streams)} verified / {total_streams} total")
            
            # Group by feed type
            feeds: dict[str, list[StreamLink]] = {}
            for stream in game.streams:
                if verified_only and not stream.verified:
                    continue
                if stream.feed_type not in feeds:
                    feeds[stream.feed_type] = []
                feeds[stream.feed_type].append(stream)
                
            for feed_type, streams in feeds.items():
                if not streams:
                    continue
                print(f"    [{feed_type}]")
                for s in streams[:10]:  # Limit to 10 per feed type
                    channel_info = f" ({s.channel})" if s.channel else ""
                    status_icon = "✅" if s.verified else "❓"
                    
                    if s.m3u8_url:
                        print(f"      {status_icon} {s.source}{channel_info}")
                        print(f"         M3U8: {s.m3u8_url}")
                        if s.extraction_method:
                            print(f"         Method: {s.extraction_method}")
                    else:
                        print(f"      {status_icon} {s.source}{channel_info}: {s.url}")
                        
                if len(streams) > 5:
                    print(f"      ... and {len(streams) - 5} more")
        elif not game.streams:
            print("  Streams: Available closer to game time")


def extract_and_verify_streams(games: list[Game], max_per_game: int = 5,
                                verbose: bool = False, verify: bool = True) -> list[Game]:
    """
    Extract actual m3u8 URLs from embed pages and verify they work.
    
    Args:
        games: List of Game objects with embed URLs
        max_per_game: Maximum streams to process per game
        verbose: Print extraction progress
        verify: Whether to verify streams after extraction
        
    Returns:
        Updated list of Game objects with m3u8 URLs populated
    """
    extractor = StreamExtractor(verbose=verbose)
    verifier = StreamVerifier(verbose=verbose) if verify else None
    
    total_games = len([g for g in games if g.streams])
    print(f"\nExtracting streams from {total_games} games...")
    
    for i, game in enumerate(games):
        if not game.streams:
            continue
            
        game_name = f"{game.home_team} vs {game.away_team}"
        print(f"\n[{i+1}/{total_games}] {game_name}")
        
        # Prioritize certain sources known to work better
        priority_sources = ["freestr", "wikisport", "fluidtv", "vklive"]
        
        def source_priority(stream):
            source_lower = stream.source.lower()
            for i, p in enumerate(priority_sources):
                if p in source_lower:
                    return i
            return len(priority_sources)
            
        sorted_streams = sorted(game.streams, key=source_priority)
        
        processed = 0
        for stream in sorted_streams:
            if processed >= max_per_game:
                break
                
            if not stream.url or not stream.url.startswith("http"):
                continue
                
            print(f"  Trying {stream.source} ({stream.feed_type})...", end=" ", flush=True)
            
            # Determine appropriate referer
            from urllib.parse import urlparse
            parsed = urlparse(stream.url)
            referer = f"{parsed.scheme}://{parsed.netloc}/"
            
            # Special case for onhockey wrapper
            if "onhockey" in stream.url:
                referer = "https://onhockey.tv/"
                
            result = extractor.extract(stream.url, referer)
            if result:
                m3u8_url, method = result
                stream.m3u8_url = m3u8_url
                stream.extraction_method = method
                print(f"✓ Found via {method}")
                
                if verifier:
                    print(f"    Verifying...", end=" ", flush=True)
                    is_valid, info = verifier.verify(m3u8_url, referer)
                    stream.verified = is_valid
                    
                    if is_valid:
                        info_str = ""
                        if info:
                            if info.get("variants"):
                                resolutions = [v.get("resolution") for v in info["variants"] if v.get("resolution")]
                                if resolutions:
                                    info_str = f" ({', '.join(resolutions)})"
                            elif info.get("width"):
                                info_str = f" ({info['width']}x{info['height']})"
                        print(f"✓ Working{info_str}")
                        processed += 1
                    else:
                        print("✗ Failed verification")
                else:
                    processed += 1
            else:
                print("✗ No stream found")
                
    return games
            

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
    parser.add_argument(
        "-e", "--extract",
        action="store_true",
        help="Extract actual m3u8 stream URLs from embed pages"
    )
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Skip stream verification (faster but less reliable)"
    )
    parser.add_argument(
        "--verified-only",
        action="store_true",
        help="Only show verified working streams"
    )
    parser.add_argument(
        "--max-streams",
        type=int,
        default=5,
        help="Maximum streams to extract per game (default: 5)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output during extraction"
    )
    
    args = parser.parse_args()
    
    # Check for required tools
    print("Checking available tools...")
    tools = {
        "curl": shutil.which("curl") is not None,
        "yt-dlp": shutil.which("yt-dlp") is not None,
        "ffprobe": shutil.which("ffprobe") is not None,
    }
    for tool, available in tools.items():
        status = "✓" if available else "✗"
        print(f"  {status} {tool}")
    
    print("\nFetching schedule from onhockey.tv...")
    games = fetch_schedule(timezone_offset=args.timezone)
    
    if not games:
        print("Failed to fetch schedule or no games found.")
        return
    
    # Apply team filter early
    if args.team:
        team_lower = args.team.lower()
        games = [g for g in games if 
                 team_lower in g.home_team.lower() or 
                 team_lower in g.away_team.lower()]
        
    # Apply league filter early
    if args.league:
        games = [g for g in games if args.league.lower() in g.league.lower()]
        
    print(f"Found {len(games)} games.\n")
    
    if not games:
        print("No games match your filters.")
        return
    
    # Extract actual stream URLs if requested
    if args.extract:
        games = extract_and_verify_streams(
            games, 
            max_per_game=args.max_streams,
            verbose=args.verbose,
            verify=not args.no_verify
        )
    
    if args.urls_only:
        # Output m3u8 URLs if extracted, otherwise embed URLs
        for game in games:
            for stream in game.streams:
                if args.verified_only and not stream.verified:
                    continue
                url = stream.m3u8_url if stream.m3u8_url else stream.url
                if url:
                    print(url)
    else:
        print_schedule(
            games,
            show_streams=not args.no_streams,
            json_output=args.json,
            verified_only=args.verified_only
        )


if __name__ == "__main__":
    main()