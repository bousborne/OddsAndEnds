vector<int> longestUncorruptedSegment(vector<int> sourceArray, vector<int> destinationArray) {
    vector<int> ans;
    int startingBlock=0;
        int curStartingBlock=0;

    bool stillGood = false;
    int count=0;
    int curCount=0;
    for(int i=0; i<sourceArray.size(); i++) {
        // count = 1;
        // if(sourceArray[i] != destinationArray[i]) {
        //     stillGood = false;
        //     count=0;
        // }
        // if(sourceArray[i] == destinationArray[i] && !stillGood) {
        //     curStartingBlock = i;
        // }
        while (sourceArray[i] == destinationArray[i]) {
            curCount++;
            i++;
            curStartingBlock = i - curCount;
			if (i >= sourceArray.size()) {
				break;
			}
        } 
        
        if (curCount > count) {
            count = curCount;
            startingBlock = curStartingBlock;
        }
        curCount = 0;
        curStartingBlock = 0;
        
    }
    ans.push_back(count);
    ans.push_back(startingBlock);
    return ans;
}
