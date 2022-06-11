import java.util.*;
import java.io.*;

class State extends GlobalSimulation{
	
	public int numberInQueue = 0, accumulated = 0, noMeasurements = 0;

	Random rndArrival = new Random(seed); 
	Random rndServer = new Random(seed+1);
	Random rndMeasure = new Random (seed+2);
	
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
	
	private void arrival(){
		numberInQueue++;
		if (numberInQueue <= 2)
			//insertEvent(DEPARTURE, time + 2.0 - (2.0*rndServer.nextDouble()));
			insertEvent(DEPARTURE, time + (2.0*rndServer.nextDouble()));
		insertEvent(ARRIVAL, time + expRndArrival(1.2));
	}
	
	private void departure(){
		numberInQueue--;
		if (numberInQueue > 1)
			//insertEvent(DEPARTURE, time + 2.0 - (2*rndServer.nextDouble()));
			insertEvent(DEPARTURE, time + (2*rndServer.nextDouble()));
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
			double squrDiffToMean = Math.pow(val - mean, 2);
			temp += squrDiffToMean;
		}


		double meanOfDiffs = (double) temp / (double) (currentNumberOfCustomers.size());


		return Math.sqrt(meanOfDiffs);
	}

}