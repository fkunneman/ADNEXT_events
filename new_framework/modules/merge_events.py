
from luiginlp.engine import Task, StandardWorkflowComponent, WorkflowComponent, InputFormat, InputComponent, registercomponent, InputSlot, Parameter, IntParameter, BoolParameter

import json
import glob
import os
import datetime 
from collections import defaultdict

from functions import event_merger
from classes import event


################################################################################
###Event integrator
################################################################################

@registercomponent
class IntegrateEvents(WorkflowComponent):

    current_events = Parameter()
    new_events = Parameter()

    overlap_threshold = Parameter(default = 0.2)

    def accepts(self):
        return [ ( InputFormat(self, format_id='current_events', extension='.integrated', inputparameter='current_events'), InputFormat(self, format_id='new_events', extension='.events', inputparameter='new_events') ) ]

    def setup(self):
        integrator = workflow.new_task('merge_events', IntegrateEventsTask, autopass=False, overlap_threshold=self.overlap_threshold)
        integrator.in_current_events = input_feeds['current_events']
        integrator.in_new_events = input_feeds['new_events']
        return integrator

class IntegrateEventsTask(Task):

    in_current_events = InputSlot()
    in_new_events = InputSlot()

    overlap_threshold = Parameter()

    def out_integrated_events(self):
        return self.outputfrominput(inputformat='new_events', stripextension='.events', addextension='.events.integrated')

    def run(self):

        # read in current events
        with open(self.in_current_events().path, 'r', encoding = 'utf-8') as file_in:
            current_eventdicts = json.loads(file_in.read())
        current_event_objs = []
        for ed in current_eventdicts:
            eventobj = event.Event()
            eventobj.import_eventdict(ed)
            current_event_objs.append(eventobj)

        # initialize event merger
        merger = event_merger.EventMerger()
        merger.add_events(current_event_objs)

        # read in new events
        with open(self.in_new_events().path, 'r', encoding = 'utf-8') as file_in:
            new_eventdicts = json.loads(file_in.read())
        new_event_objs = []
        for ed in new_eventdicts:
            eventobj = event.Event()
            eventobj.import_eventdict(ed)    
            new_event_objs.append(eventobj)    

        # merge before integration
        print('Merging new events before integration; number of events at start:',len(new_event_objs))
        premerger = event_merger.EventMerger()
        premerger.add_events(new_event_objs)
        premerger.find_merges(self.overlap_threshold)
        new_events_merged = premerger.return_events()
        print('Done. New events after merge:',len(new_events_merged))

        # integrate each event into the current ones
        print('Starting integrating new events; number of current events:',len(current_event_objs))
        for new_event in new_events_merged:
            merger.find_merge(eventobj,self.overlap_threshold)

        # write merged 
        merged_integrated = merger.return_events()
        print('Done. Number of events after integration:',len(merged_events))
        with open(self.out_integrated_events().path,'w',encoding='utf-8') as file_out:
            json.dump(events_integrated,file_out)

################################################################################
###Event merger
################################################################################

@registercomponent
class MergeEvents(WorkflowComponent):

    events = Parameter()

    overlap_threshold = Parameter(default = 0.2)

    def accepts(self):
        return InputFormat(self, format_id='events', extension='.integrated')

    def autosetup(self):
        return MergeEventsTask

class MergeEventsTask(Task):

    in_events = InputSlot()

    overlap_threshold = Parameter()

    def out_merged_events(self):
        return self.outputfrominput(inputformat='events', stripextension='.integrated', addextension='.merged')

    def run(self):

        # read in events
        with open(self.in_events().path, 'r', encoding = 'utf-8') as file_in:
            eventdicts = json.loads(file_in.read())
        event_objs = []
        for ed in eventdicts:
            eventobj = event.Event()
            eventobj.import_eventdict(ed)
            event_objs.append(eventobj)

        # initialize event merger
        print('Merging; number of events at start:',len(event_objs))
        merger = event_merger.EventMerger()
        merger.add_events(event_objs)
        merger.find_merges(self.overlap_threshold)
        events_merged = merger.return_events()
        print('Done. number of events after merge:',len(events_merged))        

        # write merged 
        with open(self.out_merged_events().path,'w',encoding='utf-8') as file_out:
            json.dump(events_merged,file_out)