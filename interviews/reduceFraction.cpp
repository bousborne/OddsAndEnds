vector<string> ReduceFraction(vector<string> fractions) {
    vector<string> ans;
    std::string delimiter = "/";
    for(auto s : fractions) {
        
        std::cout << s << ' ' << std::endl;
        size_t pos = 0;
        std::string divisor;
        std::string denominator;
        vector<string> words{};
        while ((pos = s.find(delimiter)) != string::npos) {
            words.push_back(s.substr(0, pos));
            std::cout << s.substr(0, pos);
            std::cout << pos;
            s.erase(0, pos + delimiter.length());
        }
        
        for ( auto str : words) {
            std::cout << str << std::endl;
        }
        // size_t found;
        // if ((found = s.find("/")) != string::npos) {
        //     std::cout << s.substr(0, found) << std::endl;
        //     std::cout << s.substr(found+1, string::npos) << std::endl;
        // }
        // while((pos = s.find(delimiter)) != std::string::npos) {
        //     divisor = s.substr(0, pos);
        //     std::cout << pos << std::endl;
        //     // std::cout << 
        // }
        denominator = s.substr(pos, std::string::npos);
        cout << divisor << " " << denominator << std::endl;
        // int 
    }
    return ans;
}
