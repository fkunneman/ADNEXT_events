
class EventMerger:

    def __init__(self):
        self.events = []

    def add_events(self,events):
        self.events.extend(events)

    def return_events(self):
        return self.events

    def find_merge(self,event,overlap_threshold):
        candidates = self.return_events_date(event.date)
        for candidate in candidates:
            if self.has_overlap(candidate,event,overlap_threshold):
                candidate = self.merge_events(candidate,event)
                break

    def find_merges(self,overlap_threshold)
        # sort by date
        dates = sorted(list(set([event.date for event in self.events])))
        for date in dates:
            candidates = self.return_events_date(date)
            print('Finding merges out of',len(candidates),'events on',date)
            merged = candidates[0]
            for event2 in candidates[1:]:
                for event1 in merged:
                    if has_overlap(event1,event2,overlap_threshold):
                        event1.merge(event2)
                        break
                    merged.append(event2)
            print('Merged to',len(merged),'events')

    def has_overlap(self,event1,event2,overlap_threshold):
        intersect = list(set([tweet.id for tweet in event1.tweets]) & set([tweet.id for tweet in event2.tweets]))
        overlap_percent = len(intersect) / len(event1.tweets)
        overlap = True if overlap_percent > overlap_threshold else False
        return overlap

    def return_events_date(self,date):
        return [event for event in self.events if event.date == date]