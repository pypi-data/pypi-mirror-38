.. _eventlogging:

=============
Event Logging
=============

Events are discrete & structured items emitted by
BinderHub when specific events happen. For example,
the ``binderhub.jupyter.org/launch`` event is emitted
whenever a Launch succeeds.

These events may be sent to a *sink* via handlers
from the python ``logging`` module. 

Events vs Metrics
=================

BinderHub also exposes `prometheus <https://prometheus.io>`_
metrics. These are pre-aggregated, and extremely limited in
scope. They can efficiently answer questions like 'how many launches
happened in the last hour?' but not questions like 'how
many times was this repo launched in the last 6 months?'. 
Events are discrete and can be aggregated in many ways
during analysis. Metrics are aggregated at source, and this
limits what can be done with them during analysis. Metrics
are mostly operational, while events are for analytics.

What events to emit?
====================

Since events have a lot more information than metrics do,
we should be careful about what events we emit. In general,
we should pose an **explicit question** that events can answer.

For example, to answer the question *How many times has my
GitHub repo been launched in the last 6 months?*, we would need
to emit an event every time a launch succeeds. To answer the
question *how long did users spend on my repo?*, we would need
to emit an event every time a user notebook is killed, along
with the lifetime length of the notebook.

`Wikimedia's EventLogging Guidelines <https://www.mediawiki.org/wiki/Extension:EventLogging/Guide#Posing_a_question>`_
contain a lot of useful info on how to approach adding more events.