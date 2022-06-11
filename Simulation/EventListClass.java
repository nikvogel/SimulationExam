
public class EventListClass {
	
	private Event list, last; 
	
	EventListClass(){
		list = new Event();
    	last = new Event();
    	list.next = last;
	}
	
	
	public void InsertEvent(int type, double TimeOfEvent){
 	Event dummy, predummy;
 	Event newEvent = new Event();
 	newEvent.eventType = type;
 	newEvent.eventTime = TimeOfEvent;
 	predummy = list;
 	dummy = list.next;
 	while ((dummy.eventTime < newEvent.eventTime) & (dummy != last)){
 		predummy = dummy;
 		dummy = dummy.next;
 	}
 	predummy.next = newEvent;
 	newEvent.next = dummy;
 }
	
	public Event fetchEvent(){
		Event dummy;
		dummy = list.next;
		list.next = dummy.next;
		dummy.next = null;
		return dummy;
	}
}