import java.util.*;
import java.io.*;

public class MainSimulation extends GlobalSimulation{
	static FileWriter writerMeasurements; 
 
    public static void main(String[] args) throws IOException {
		ArrayList meanCustomerList = new ArrayList<Double>();
		writerMeasurements = new FileWriter("Measurements.csv"); 

		for(int i=0; i<100; i++){
			meanCustomerList.add(runSimulation(i));
		}
		writerMeasurements.close();
		writeToCsv(meanCustomerList, "MeanCustomersInQueue0.csv");
    }

	public static double runSimulation(int i) throws IOException{
		time = 0;
		seed = i;
		sdMean = 100.0;
		currentNumberOfCustomers = new ArrayList<Integer>();
		eventList = new EventListClass();
		Event actEvent;
    	State actState = new State(); 
        insertEvent(ARRIVAL, 0);  
        insertEvent(MEASURE, 5);
        
        
    	while (sdMean > 0.01){
    		actEvent = eventList.fetchEvent();
    		time = actEvent.eventTime;
    		actState.treatEvent(actEvent);
    	}
    	
    	double meanCustomers = 1.0*actState.accumulated/actState.noMeasurements;

		writeMeasurements(currentNumberOfCustomers);

		System.out.println("Mean customers: " + meanCustomers);
		System.out.println("Standard Dev: " + sdMean);
		System.out.println("Measurements: " + actState.noMeasurements);

		return meanCustomers;
	}

	public static void writeToCsv(ArrayList list, String filename) throws IOException{
		FileWriter writer = new FileWriter(filename); 
		for (Object dd:list)
			writer.write(dd + System.lineSeparator());
		writer.close();
	}

	public static void writeMeasurements(ArrayList list) throws IOException{
		for (Object dd:list)
			writerMeasurements.write(dd + System.lineSeparator());
	}


}