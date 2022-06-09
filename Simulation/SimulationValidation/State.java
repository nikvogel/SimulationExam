import java.util.*;
import java.io.*;

class State extends GlobalSimulation{
	
	// Here follows the state variables and other variables that might be needed
	// e.g. for measurements
	public int numberInQueue = 0, accumulated = 0, noMeasurements = 0;

	Random rndArrival = new Random(seed); // This is just a random number generator
	Random rndServer = new Random(seed+1);
	Random rndMeasure = new Random (seed+2);
	
	// The following method is called by the main program each time a new event has been fetched
	// from the event list in the main loop. 
	public void treatEvent(Event x){
		switch (x.eventType){
			case ARRIVAL:
				arrival();
				break;
			case DEPARTURE:
				departure();
				break;
			case MEASURE:
				measure();
				break;
		}
	}
	
	
	// The following methods defines what should be done when an event takes place. This could
	// have been placed in the case in treatEvent, but often it is simpler to write a method if 
	// things are getting more complicated than this.
	
	private void arrival(){
		numberInQueue++;
		if (numberInQueue <= 2)
			insertEvent(DEPARTURE, time + (expRndService(1.0)));
		insertEvent(ARRIVAL, time + expRndArrival(1.2));
	}
	
	private void departure(){
		numberInQueue--;
		if (numberInQueue > 1)
			insertEvent(DEPARTURE, time + (expRndService(1.0)));
	}
	
	private void measure(){
		accumulated = accumulated + numberInQueue;
		noMeasurements++;
		currentNumberOfCustomers.add(numberInQueue);
		if (currentNumberOfCustomers.size()>10)
			sdMean = 1.0*sd()/Math.sqrt(noMeasurements);
			//System.out.println(sdMean);
		insertEvent(MEASURE, time + expRndMeasure(5));
	}

	public double expRndArrival(double expectedValue) {
		//return (Math.log(1.0 - rndArrival.nextDouble())/(-1.0/expectedValue));
		return (Math.log(rndArrival.nextDouble())/(-1.0/expectedValue));
	}

	public double expRndService(double expectedValue) {
		//return (Math.log(1.0 - rndServer.nextDouble())/(-1.0/expectedValue));
		return (Math.log(rndServer.nextDouble())/(-1.0/expectedValue));
	}

	public double expRndMeasure(double expectedValue) {
		//return (Math.log(1.0 - rndMeasure.nextDouble())/(-1.0/expectedValue));
		return (Math.log(rndMeasure.nextDouble())/(-1.0/expectedValue));
	}

	public static double sd (){
		Double mean = currentNumberOfCustomers
							.stream()
							.mapToInt(a -> a)
							.average()
							.orElse(-1);
		double temp = 0;
		for (int i = 0; i < currentNumberOfCustomers.size(); i++)
		{
			int val = currentNumberOfCustomers.get(i);

			// Step 2:
			double squrDiffToMean = Math.pow(val - mean, 2);

			// Step 3:
			temp += squrDiffToMean;
		}


		double meanOfDiffs = (double) temp / (double) (currentNumberOfCustomers.size());


		return Math.sqrt(meanOfDiffs);
	}

}