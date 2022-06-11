import java.util.*;

public class GlobalSimulation{
	
	public static final int ARRIVAL = 1, DEPARTURE = 2, MEASURE = 3; 
	public static double time = 0; 
	public static double sdMean;
	public static int seed;
	public static ArrayList<Integer> currentNumberOfCustomers = new ArrayList<Integer>();
	public static EventListClass eventList = new EventListClass(); 
	public static void insertEvent(int type, double TimeOfEvent){  
		eventList.InsertEvent(type, TimeOfEvent);
	}
}