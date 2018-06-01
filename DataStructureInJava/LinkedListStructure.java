// One direction Linked list
// Data are stored in the form of (data,address)

import java.util.Scanner;

public class LinkedListStructure{
	public static void main(String[] args){

		Node node, head = null;
		LinkedList linkedList = new LinkedList();
		String key;
		Scanner input = new Scanner(System.in);
		System.out.println("Input data in the form of (key, name, age). Input age 0 to end.");

		while(true){
			// get input data
			DATA dataInNode = new DATA();
			System.out.print("key: ");
			dataInNode.key = input.next();
			System.out.print("name: ");
			dataInNode.name = input.next();
			System.out.print("age: ");
			dataInNode.age = input.nextInt();
			// if end
			if (dataInNode.age == 0){
				break;
			}
			else{
				head = linkedList.addingAtEnd(head, dataInNode);
			}
		}
		System.out.println("Input done.");
		// print all data
		linkedList.printAllInfo(head);

		// Insersion demo
		System.out.println("Insersion demo: input the key of the target node: ");
		key = input.next();
		System.out.println("Input data of the new node: ");
		DATA dataInNode = new DATA();
		System.out.print("key: ");
		dataInNode.key = input.next();
		System.out.print("name: ");
		dataInNode.name = input.next();
		System.out.print("age: ");
		dataInNode.age = input.nextInt();
		head = linkedList.insertNode(head, key, dataInNode);
		System.out.println("Done.\n\nNew list: \n");
		linkedList.printAllInfo(head);

		//deletion demo
		System.out.println("Deletion demo: input the key of the target node: ");
		key = input.next();
		linkedList.deleteNode(head,key);
		System.out.println("Done.\n\nNew List:\n");
		linkedList.printAllInfo(head);

		// Search demo
		System.out.println("Searching demo: input the key of the target node: ");
		key = input.next();
		node = linkedList.findNode(head,key);
		if (node!=null) {
			System.out.println("Target node: "+node.dataInNode.key+" "+node.dataInNode.name+" "+node.dataInNode.age);		
		}

	}

}	

class DATA{

	String key;
	String name;
	int age;

}

class Node{
	// constructor

	DATA dataInNode = new DATA();
	Node nextNode;

    
}

class LinkedList{

    Node head = new Node();  
 
	// adding node at the end of the linked list, return the head.
	Node addingAtEnd(Node head, DATA dataInNode){

		Node node, tempNode;
		// check memory distributing
		if ((node = new Node()) == null) {
			System.out.println("Memory distributing failed..");		
			return null;
		}
		else{
			// store data in the new node
			node.dataInNode = dataInNode;
			node.nextNode = null;
			// store address of the next ndoe in the new node
			//
			//if the linked list does not yet have a head
			if (head == null) {
				head = node;
				return head;
			}
			else{
				// searching for the end of the list, and set the address to the new node
				tempNode = head;
				while(tempNode.nextNode!=null){
					tempNode=tempNode.nextNode;
				} 
				tempNode.nextNode = node;
				return head;
			}
		}
	}


	// adding new head to the list
	Node addingHead(Node head, DATA dataInNode){

		Node node;

		// check memory distributing
		if ((node = new Node()) == null) {
			System.out.println("Memory distributing failed..");		
			return null;
		}
		else{
			node.dataInNode = dataInNode;
			node.nextNode = head;
			head = node;
			return head;
		}		
	}


	// insert node
	// find the insertion place by key
	Node insertNode(Node head, String key, DATA dataInNode){

		Node node, tempNode;

		// check memory distributing
		if ((node = new Node()) == null) {
			System.out.println("Memory distributing failed..");		
			return null;
		}
		else{
			//store data
			node.dataInNode = dataInNode;
			//check address
			tempNode = findNode(head, key);
			//if the given location is null
			if(tempNode == null){
				System.out.println("Unexpected insertion location..");
				// free the memory given to node
				tempNode.dataInNode=null;
				tempNode=null;
			}
			else{
				// set the nextnode of the inserted node to be the next node of the key node
				node.nextNode = tempNode.nextNode;
				// and set the next node of the key node to be the inserted node
				tempNode.nextNode = node;
			}
		}
		return head;
	}

	// find a node
	Node findNode(Node head, String key){

		Node tempNode;
		tempNode = head;

		// if the node is valid, continue searching
		while(tempNode != null){
			// if find the target key
			if(tempNode.dataInNode.key.compareTo(key) == 0){
				return tempNode;
			}
			else{
				// if doesn't find, countinue checking the next node
				tempNode = tempNode.nextNode;
			}
		}
		System.out.println("Target node not found.");
		return null;
	}

	// detete a node
	boolean deleteNode(Node head, String key){

		Node node, tempNode;

		tempNode = head;
		node = head;
		// if the node is valid, continue searching		
		while(tempNode != null){
			// if not find the target key, move to the next ndoe
			if(tempNode.dataInNode.key.compareTo(key) != 0){
				//use node to refer to the previous node of the target node
				//use tempNode to find the target node.
				node = tempNode;
				tempNode = tempNode.nextNode;
			}
			// if find, set the nextnode of the node one position before the target node to 
			// be the nextnode of the target node.
			else{
				node.nextNode = tempNode.nextNode;
				tempNode.dataInNode=null;
				tempNode=null;
				return true;
			}
		}
		System.out.println("Deletion failed..");
		return false;
	}

	// find the length of a linked list
	int length(Node head){

		Node tempNode;
		tempNode = head;
		int length = 0;

		// till the end
		while(tempNode != null){
			tempNode = tempNode.nextNode;
			length++;
		}

		return length;
	}

	// show all info in the list
	void printAllInfo(Node head){

		Node tempNode;
		tempNode = head;
		System.out.println("There are "+length(head)+"nodes in the current list.\nInfo: \n");
		// print the info of each node
		while(tempNode != null){
			System.out.println(tempNode.dataInNode.key+tempNode.dataInNode.name+tempNode.dataInNode.age);
			tempNode = tempNode.nextNode;
		}
	}


}