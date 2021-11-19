//Given an array of pairs of integers where the pair represents the start and end point of a 1D line segment, write a function to output an array of the same format, where the lines cover the same range of values but with the minimum number of segments, i.e. merge any overlapping segments.

//Example input:      [ (2,5) , (1,3) , (7,9) ]
//Expected output:   [ (1,5) , (7,9) ]

// [  (1,3), (2,10) , (7,9) ]

// currStart = 7
// currEnd = 9

vector<pairs<int,int>> lineConverge(vector<ints> input) {
    vector<pair<int,int>> answer;

mergeSort(input, input.size()); // sort on x value of pair

Int currStartPoint = input[0]->first;
Int currEndPoint = input[0]->second;

// [  (1,10), (2,3) , (7,9) ]
[(1,10)

[ (1,3)  (2,5) ,, (7,9) ]
// 1, 3
 For (int j=1; j < input.size(); j++) {
    //

    If (input[j]->first <= currEndPoint ) {
        std::max(input, )
        If (input[j]->second <= input[j-1]->second) {
            currEndPoint = input[j-1]->second;
        } else {
            currEndPoint = input[j]->second;
}
    } else {
        answer.push_back(make_pair(currStartPoint, currEndPoint));
        currStartPoint = input[j]->first;
        currEndPoint = input[j]->second;
    }
}
answer.push_back(make_pair(currStartPoint, currEndPoint));

    Return answer;
}

