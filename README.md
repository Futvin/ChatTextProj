# snaptext

This is a simple API type web interface for an ephemeral text message service.

## Running this application

### Prerequisites

You will need to run this from a host with Docker installed plus all normal tools such as docker-compose.  You will also need an internet connection.  This was developed against Docker version 18, and may not work properly on earlier versions of docker.

### Build and Start the application

You can build and start up the application using docker-compose:

```
docker-compose up --build -d
```

You can also build the application, then run it in two steps.  E.g.

```
docker-compose build
docker-compose up -d
```

By default, this application will listen on port ___80___ of your system.  You can change this in the docker-compose.yml file.

## Design considerations

This project was to create a small application, very quickly, that has potential to scale.

I chose to use Python because it is very fast to develop with, yet it is robust and can scale well.  I chose the Flask framework because it is very light weight, quick to build with, and great for API framework.

I am using a Mongo database, because it is a vary robust NoSQL database designed so that it can scale to very large datasets.  The message format very easily lends itself to a NoSQL document database.

I am using redis for my message ID so that I can have one centralized authority for my message ID, to ensure that it will be unique.  Redis is again, another robust NoSQL database that can be setup in a redundant fashion for reliability.

I wrapped this up in Docker because this too allows this application to be well defined (by Docker files or pulled images).  Currently, this application is extremely light weight, and docker containers would allow this application to stay this way.  However, Docker make it easy to scale up this applications, given then correct backend configuration.  With docker, each virtual system configuration is done in code which makes it easy to adjust in the future.  Finally, the development version and the production systems will work the same because they are the same systems.  The only differences will come when the system is scaled onto something like a Docker swarm / Kubernetes managed Docker cluster.

All of these technologies are fairly common and will be easy to support by me or other people.

## Limitations of this design

1.  For extremely high volumes, python may prove to be too slow, even if it is scaled out to many nodes.  A complied language like C/C++, Go, Rust, etc, may make more sense in those cases.

2.  Adding redis was useful for getting the next numerical ID in a synchronized, atomic way.  It would make more sense to use an alpha-numeric id for the message so that more messages could be handled.  In this cause a different system, or just relying on the mongo id could work.  This will make the IDs smaller as the database grows to be very large.

3.  No indexes have been created in the mongo DB.  So queries will start to slow down with larger data sets.  An index on the username field would be the most important one, as this is how the customers query the data.

4.  At this point, the application will not do any autoscaling.  Most likely this will something that is configured at the container orchestration layer.  If a lot of traffic is anticipated, then starting the databases as a small cluster would make more sense, instead of trying to migrate them to that configuration.

The application in and of its self will do fine for scaling.  However, if the container orchestration does not include a load balancer.  Then something like an elastic IP address, or something like an HAProxy set of system can balance the traffic.

Furthermore, the application just goes to The Mongo instance and The Redis instance.  This may need to be abstracted, or at least directed to the cluster of leader instances.  Most likely the redis instance would only need to scale to two for redundancy.

5.  There is no security with this application.

Generally, using a framework like Flask as the receiver of web traffic is considered bad form because it does not have inherent security, and it is more secure to have this behind an apache/nginx server.  This could be ok, if this was purely internal.

The data is all in plan text, which is probably fine for how this application is used.

If the /chat/$id API is for admins, then it would be nice to lock this down, depending on how it is accessed.

6.  In a production setting, I would like to use automation for deployment instead of doing that by hand.  Additionally, version information in the application could be nice.  These aren't problems with the application, but rather the management of the application and its life cycle.


### What I would do with more time.

1.  I did not put in a lot of exception handling.  Edge case testing and development would be good.

2.  The example request body is malformed json.  If that is real world data, then I would need to update my code to handle that.

3.  I would add an index on username in the Mongo DB, as mentioned above.  I am sure that will become a problem as thousands of entries appear on the system.

### How would I scale this in the future

The basic configuration for high loads of traffic would roughly look like this:

_load balancers (elastic IPs or HAProxy, etc)_
      / | \
_many snaptext containers_
      / | \                       / | \
_a cluster of mongo DBs - one or two redis DBs_

Incoming traffic is split between many systems running the front end APIs.  Then all of those systems would interact with a cluster of databases in the back end.

#### Scaling for very high data sets

There will be some issues as the data gets to be very large.  The NoSQL database is great for handling large data sets.  For trillions of chat messages, for instance, a well index query may still take a very long time.  In this case, it would be better to split up the database into much smaller chunks (say thousdands of databases of a billion messages).  With this, the application would run a query for a username against each database in a separate thread.  Those results would then be sent to a master process that would glue the results together and send it along.  Basically like MapReduce, except there is no true reduction.
