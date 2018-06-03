private void start()
{
	//
	//initialize the map with blank cells.
	//
	for(int i = 0; i<(row*col);i++)
	{
		realMap[i] = BLANK;
	}
	Random randMap = new Random();
	//
	//Genrate random maps
	//Put all pairs of images into a temporary map.
	//	
	ArrayList tmpMap = new ArrayList;
	for(int i = 0; i<row*col/4;i++)
	{
		for(int j = 0; j <4; j++)
		{
			tempMap.add(i);
		}
	}
	//
	//Transfer images from the temporary map to the blank map.
	//
	for (int i = 0; i< row*col; i++)
	{
		//
		//random place to put
		//
		int index = randMap.nextInt(tmpMap.size());
		realMap[i] = (Integer)tmpMap.get(index);
		tmpMap.remove(index)
	}
}

boolean deletable(int x1, int x2, int y1, int y2)
{
	//Vertically
	if(x1 == x2)
	{
		if (verticallyDeletable(x1,y1,y2))
		{
			lType = LinkType.LineType;
			return true;
		}
	}

	//Horizontally
	else if(y1 == y2)
	{
		if (horizontallyDeletable(x1,x2,y1))
		{
			lType = LinkType.LineType;
			return true;
		}
	}

	//One curve
	if(deletableWithOneCorner(x1,x2,y1,y2))
	{			
		lType = LinkType.LineType;
		return true;
	}

	//Two curves
	else if (deletableWithTwoCorners(x1,x2,y1,y2))
	{
		lType = LinkType.LineType;
		return true;
	}

	return false;
}

boolean verticallyDeletable(int x, iny y1, int y2)
{
	if(y1>y2)
	{
		int temp = y1;
		y1 = y2;
		y2 = temp;
	}

	for (int i = y1+1; i<= y2; i++)
	{
		if(i == y2)
		{
			return true;
		}
		if(realMap[i*col+x]!=BLANK)
		{
			break;
		}
	}
	return false;
}

boolean horizontallyDeletable(int x1, int x2, int y)
{
	if(x1<x2)
	{
		int temp = x1;
		x1 = x2;
		x2 = temp;
	}

	for (int i = x1+1; i<= x2; i++)
		{
			if(i == x2)
			{
				return true;
			}
			if(realMap[y*col+i]!=BLANK)
			{
				break;
			}
		}
	return false;
}

boolean deletableWithOneCorner(int x1, int x2, int y1, int y2)
{
	if(x1<x2)
	//
	//switch point(x1,y1) and point(x2,y2)
	//
	{
		int temp = x1;
		x1 = x2;
		x2 = temp;
		temp = y1;
		y1=y2;
		y2=temp;
	}
	//
	//if two points in lowerleft-upperright diagonal
	//
	if (y2<y1){
		//
		//see if the lowerright corner is empty
		//
		if (realMap[y1*col+x2]==BLANK)
		{
			//
			//see if the two points are directly approachable
			//
			if(verticallyDeletable(x2,y1,y2)&&horizontallyDeletable(x1,y1,y2))
			{	
				//
				//save the coordinate to the corner point
				//
				corner1.x = x2;
				corner1.y = y1;
				return true;
			}
		}
		//
		//see if the upperleft corner is empty
		//
		if (realMap[y2*col+x1]==BLANK)
		{
			//
			//see if the two points are directly approachable
			//
			if (verticallyDeletable(x2,y1,y2)&&horizontallyDeletable(x1,y1,y2))
			{	
				//
				//save the coordinate to the corner point
				//
				corner1.x = x1;
				corner1.y = y2;
				return true;
			}
		}
		return false;
	}
	//
	// if point(x1,y1)is at the upperleft corner and (x2,y2) is at the lowerrigght corner
	//
	else
	{
		//
		//see if the lowerleft corner is empty
		//
		if (realMap[y2*col+x1]==BLANK) 
		{	
			//
			//see if the two points are directly approachable
			//
			if (verticallyDeletable(x2,y1,y2)&&horizontallyDeletable(x1,y1,y2))
			{
				//
				//save the coordinate to the corner point
				//
				corner1.x = x1;
				corner1.y = y2;
				return true;
			}	
		}
		//
		//see if the upperright corner is empty
		//
		if (realMap[y1*col+x2]==BLANK)
		{
			//
			//see if the two points are directly approachable
			//
			if (verticallyDeletable(x2,y1,y2)&&horizontallyDeletable(x1,y1,y2))
			{
				//
				//save the coordinate to the corner points
				//
				corner1.x = x2;
				corner1.y = y1;
				return true;
			}
		}
		return false;
	}
}

boolean deletableWithTwoCorners(int x1, int x2, int y1, int y2)
{
	if (x1>x2)
	{	
		int temp = x1;
		x1 = x2;
		x2 = temp;
		temp = y1;
		y1=y2;
		y2=temp;
	}
	//
	//right side
	//
	int x, y;

	for (x=x1+1;x<col;x++) 
	{	
		if(x == col){
			//
			//if the two coners are at the right side of the selected cell
			//
			if (verticallyAccessible(x2+1,y2,1))
			{			
				corner1.x = col;
				corner1.y = y2;
				corner2.x = col;
				corner2.y = y1;
				return true;
			}else{
				break;
			}
		}
		if (realMap[y1*col+x]!=BLANK) {
			break;
		}
		if (deletableWithOneCorner(x,x2,y1,y2)) 
		{
			corner2.x = x;
			corner2.y = y1;	
			return true;
		}
	}

	//
	// left side
	//
	for (x = x1-1; x >= -1 ; x-- ) 
	{
		if (x == -1)
			{if (verticallyAccessible(x2-1,y2,0))
				{
					corner2.x = -1;
					corner2.y = y1;
					corner1.x = -1;
					corner1.y = y2;
					return true;
			}else{
					break;
				}
		}
		
		if (realMap[y1*col+x] != BLANK)
		{
			break;
		}
		if (deletableWithOneCorner(x,x2,y1,y2)) 
		{
			corner2.x = x;
			corner2.y = y1;
			return true;
		}
	}
	//
	// Above
	//
	for (y = y1-1; y >= -1; y--) 
	{
		//
		// if the two corners are above the selected shell
		//
		if (y == -1) {
			if horizontallyAccessible(x2, y2-1, 0){
				corner2.x = x1;
				corner2.y = -1;
				corner1.x = x2;
				corner1.y = -1;
				return true;
			}else{
				break;
			}				
		}
		if (realMap[y*col+x1]!=BLANK) {
			break;
		}
		if (deletableWithOneCorner(x1,x2,y1,y2)) {
			corner2.x = x1;
			corner2.y = y;
			return true;	
		}
	}
	//
	// Down
	//
	for (y = y1+1;y<= row; y++ ) {
		//
		// if the two corners are below
		//
		if (y == row) {
			if (horizontallyAccessible(x2,y2+1,1)) {
				corner2.x = x1;
				corner2.y = row;
				corner1.x = x2;
				corner1.y = row;
				return true;	
			}else
				break;
		}		
		if (realMap[y*col+x1]!=BLANK) {
			break;
		}
		if (deletableWithOneCorner(x1,x2,y,y2)) {
			corner2.x = x1;
			corner2.y = y;
			return true;
		}
	}
	return false;
}

boolean verticallyAccessible( int x, int y, int direction){
'''decides the horizonal accesability
'''
	//
	// let 1 represent right and 0 represent left
	//
	if (direction == 1) {
		for (int i = x; i<col;i++ ) {
			if (realMap[y*col+i]!=BLANK)
				return false;
		}else{
			for (int i = 0 ; i <= x; i++) {
				if (realMap[y*col+i]!=BLANK) 
					return false;					
			}
		}
	}
}

boolean verticallyAccessible( int x, int y, int direction){
'''decides the vertical accesability
'''
	//
	// let 1 represent down and 0 represent up
	//
	if (direction == 1) {
		for (int i = x; i<row;i++ ) {
			if (realMap[i*col+x]!=BLANK)
				return false;
		}
	}else{
		for (int i = 0 ; i <= y; i++) {
			if (realMap[i*col+x]!=BLANK) 
				return false;					
			}
		}
	return true;
}

private boolean hint(){
'''finds a potential solution. Draws the hint line and returns if any solution is found.
'''
	boolean found = false;
	//
	//for thr first cell
	//
	for (int i = 0; i<row*col; i++) {
		if (found){
			break;
		}
		//
		//skip blank cells
		//
		if (realMap[i] == BLANK) {
			continue;		
		}
		//
		//check the second cell. Start from one cell after the first one
		//
		for (int j = i+1; j<col*row; j++) {
			//
			//if the second cell has the  same pattern as the first one
			//
			if (realMap[j]!=BLANK)&&(realMap[j]==realMap[i])) {
				//
				//get cordianates
				//
				x1 = i % col;
				x2 = j % col;
				y1 = i/col;
				y2 = j/col;

				//
				//see if accessible
				//
				if (deletable(x1,x2,y1,y2)){
					found = true;
					break;
				}
			}	
		}
	}
	//
	//if found, draw and return true.
	//
	if (found){
		Graphics2D hintLine = (Graphics2D) this.getGraphics;
		hintLine.setColor(Color.PINK);
		BasicStroke s = new BasicStroke(4);
		hintLine.setStroke(s);
		hintLine.drawRect(x1*W +1+W,y1*W+1+W,W-3.W-3);
		hintLine.drawRect(x2*W +1+W,y2*W+1+W,W-3.W-3;	
	}
	return found;
}
