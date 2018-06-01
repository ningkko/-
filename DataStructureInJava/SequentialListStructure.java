// Sequential list
import java.util.Scanner;

public class SequentialListStructure{
	public static void main(String[] args){
		int i;
		SequentialList SL = new SequentialList();

		SL.SLInit(SL);
		Scanner input = new Scanner(System.in);

		System.out.println("Input new data here in String ID, String name, int age: ");
		System.out.print("If end, input all 0s.");

		while (true){
			System.out.println("\nInput new data:");
			// check if done
			// store new data
			DATA data  = new DATA();
			System.out.print("ID: ");
			data.ID = input.next();
			System.out.print("Name: ");
			data.name = input.next();
			System.out.print("Age: ");
			data.age = input.nextInt();


			// if can't add, break
			if (data.age!=0){
				if(SL.add(SL,data)==false){
					break;
				}
			}
			else{
				break;
			}

		}

		System.out.println("Input done\n");
		System.out.println("all info:\n");
		SL.printAllInfo(SL);
 		
 		// Get info by inputting the number
		System.out.println("Get info by number: ");
		i = input.nextInt();
		DATA aData;
		aData = SL.getInfoByNumber(SL,i);
		if (aData!=null){
			System.out.println("The info on the "+i+"th position: "+aData.ID+" "+aData.name+" "+aData.age);
		}

		// get info by inputting ID
		System.out.println("Get info by ID: ");
		String ID;
		ID = input.next();
		i = SL.getNumByID(SL,ID);
		aData = SL.getInfoByNumber(SL,i);
		if (aData!=null){
			System.out.println("The info with ID "+ID+ "is on the "+i+"th position. Full info: "+aData.ID+" "+aData.name+" "+aData.age);
		}

		// if the user wants to delete info
		System.out.println("Delete no.: ");
		i = input.nextInt();
		if (SL.delete(SL,i)==true){
			System.out.println("Succeed.");
		}
		
	}
		
}

class DATA{

	String ID;
	String name;
	int age;

}

class SequentialList{

	static final int MAXLEN = 100;
	DATA[] DataList = new DATA[MAXLEN+1];
	int length;

	// initialize the. sequential list as an empty list
	void SLInit(SequentialList SL){
		SL.length = 0;
	}

	// lenth getter
	int getLenth(SequentialList SL){
		return SL.length;
	}

	//insert function(new data)
	boolean instert(SequentialList SL, int n, DATA data){
		int i;
		// if the list is full
		if (SL.length>=MAXLEN) {
			System.out.println("LIST FULL, CAN'T INSERT.\n");
			return false;
		}
		// insert at wrong place
		if (n<1||n>SL.length-1) {
			System.out.println("CAN'T INSERT AT POSITION "+n+".\n");
			return false;
		}
		else{
			// move all data after the nth one one position back
			for(i=SL.length;i>=n;i--){
				SL.DataList[i+1]=SL.DataList[i];
			}
			SL.DataList[n]=data;
			return true;
		}		
	}

	// add new data to the end of the list
	boolean add(SequentialList SL, DATA data){
		if (SL.length>=MAXLEN) {
			System.out.println("LIST FULL, CAN'T INSERT.\n");
			return false;			
		}
		else{
			SL.DataList[++SL.length]=data;
			return true;
		}
	}

	// delete info from thesequential list
	boolean delete(SequentialList SL, int n){
		int i;
		// no need for checking the length since all situations contained in checking position
		// if the deletion doens't happen at a right place
		if (n<1||n>SL.length-1){
			System.out.println("CAN'T DELETE AT POSITION "+n+"\n");
			return false;
		}
		else{
			// move data from after the nth one one position forward
			for(i = n;i<SL.length;i++){
			SL.DataList[i+1]=SL.DataList[i];
			}
			SL.DataList[SL.length] = null;
			SL.length--;
			return true;
		}
	}

	// get info by number
	DATA getInfoByNumber(SequentialList SL, int n){
		// jf length not right, return null
		if (n<1||n>SL.length) {
			System.out.println("TARGET POSITION LARGER THAN LIST LENGTH.\n");
			return null;
		}
		return SL.DataList[n];
	}

	// get info by ID words
	int getNumByID(SequentialList SL, String ID){
		int i;
		//compare with every id.
		for (i = 1; i<=SL.length;i++) {
			if (SL.DataList[i].ID.compareTo(ID) == 0) {
				return i;					
				}
			}
		return 0;
	}

	// a brunch of setter functions
	boolean setNameByID(SequentialList SL, String ID, String name){
		int i;
		for (i = 1; i<=SL.length;i++) {
			if (SL.DataList[i].ID.compareTo(ID) == 0) {
				SL.DataList[i].name = name;	
				return true;		
				}
		}
		return false;	
		
	}

	boolean setAgeByID(SequentialList SL, String ID, int age){
		int i;
		for (i = 1; i<=SL.length;i++) {
			if (SL.DataList[i].ID.compareTo(ID) == 0) {
				SL.DataList[i].age = age;	
				return true;		
				}
		}
		return false;	
	
	}

	boolean setAgeByName(SequentialList SL, String name, int age){
		int i;
		for (i = 1; i<=SL.length;i++) {
			if (SL.DataList[i].name.compareTo(name) == 0) {
				SL.DataList[i].age = age;	
				return true;		
				}
		}
		return false;	

	}

	boolean setIDByName(SequentialList SL, String name, String ID){
		int i;
		for (i = 1; i<=SL.length;i++) {
			if (SL.DataList[i].name.compareTo(name) == 0) {
				SL.DataList[i].ID = ID;	
				return true;		
				}
		}
		return false;	

	}

	void printAllInfo(SequentialList SL){
		int i;
		for (i = 1; i<=SL.length;i++) {
			System.out.println(SL.DataList[i].ID+SL.DataList[i].name+SL.DataList[i].age);		
		}
	}
}
