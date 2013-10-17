__package__ = "srmparserlite.splGeneral"
r"""
TODO: 1. a set contains {time, info, type, (data, bundle)}
   info : (tid, loginfo, class, ctxID, connId)

TODO: 2. if no time, will match first dir's start time agaist second dir's start time
   then apply rest of the criteria

TODO: 3. if only one time for first dir, will match the time against the second dir then
   apply rest of the criteria

TODO: 4. if both have time, then find the rest of the criteria against these period of
   time

TODO: 5. AND SET : info.tid and info.loginfo and info.class and info.ctxID and info.connID
   and type and datastring (data & bundle)

TODO: 6. OR SET : all ors

TODO: 7. combine "AND" and "OR" sets

TODO: 8. criteria file: term_{nu}.spl
   if read from *.spl , then result would be *_spl.log

spl format:
time=""


"""
