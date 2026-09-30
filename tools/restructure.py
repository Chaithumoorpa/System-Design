import os,re,subprocess,glob
R='/home/user/System-Design'
os.chdir(R)
cs='05-case-studies/'
moves={
# problems
cs+'Basics/URLShortener/README.md':'07-Basic-Questions/URL-Shortener/README.md',
cs+'Basics/RateLimiter/README.md':'15-Distributed-Infrastructure/Rate-Limiter/README.md',
cs+'Basics/UniqueIdGenerator/README.md':'05-Interview-Patterns/19-generating-unique-ids.md',
cs+'Real-Time-Communication/ChatSystem/README.md':'08-Real-Time-Communication/WhatsApp/README.md',
cs+'Real-Time-Communication/NotificationService/README.md':'17-Asynchronous-Systems/Notification-Service/README.md',
cs+'Social-and-Content/NewsFeed/README.md':'09-Social-Media-Systems/FB-News-Feed/README.md',
cs+'Social-and-Content/TopKTrending/README.md':'16-Counting-and-Ranking-Systems/Top-K/README.md',
cs+'Media-and-Storage/VideoStreaming/README.md':'10-Media-Streaming-and-Delivery/YouTube/README.md',
cs+'Media-and-Storage/FileStorageSync/README.md':'10-Media-Streaming-and-Delivery/Google-Drive/README.md',
cs+'Location-Based-Services/RideHailing/README.md':'11-Location-Based-Services/Uber/README.md',
cs+'Location-Based-Services/NearbyPlaces/README.md':'11-Location-Based-Services/Nearby-Places-Bonus/README.md',
cs+'Search-and-Discovery/Typeahead/README.md':'12-Search-and-Aggregation-Systems/Search-Autocomplete/README.md',
cs+'Search-and-Discovery/WebCrawler/README.md':'12-Search-and-Aggregation-Systems/Web-Crawler/README.md',
cs+'Commerce-and-Payments/TicketBooking/README.md':'13-E-commerce-and-Marketplace/Movie-Booking/README.md',
cs+'Commerce-and-Payments/FlashSaleInventory/README.md':'13-E-commerce-and-Marketplace/Flash-Sale/README.md',
cs+'Commerce-and-Payments/PaymentSystem/README.md':'14-Payment-and-Financial-Systems/Payment-System/README.md',
cs+'Distributed-Infrastructure/DistributedCache/README.md':'15-Distributed-Infrastructure/Distributed-Cache/README.md',
cs+'Distributed-Infrastructure/KeyValueStore/README.md':'15-Distributed-Infrastructure/Key-Value-Store/README.md',
cs+'Distributed-Infrastructure/JobScheduler/README.md':'17-Asynchronous-Systems/Job-Scheduler/README.md',
cs+'Distributed-Infrastructure/MetricsLoggingPipeline/README.md':'17-Asynchronous-Systems/Monitoring-and-Alerting/README.md',
# tips / intro / concepts
'00-getting-started/interview-framework.md':'06-Interview-Tips/01-answering-framework.md',
'01-foundations/01-estimation.md':'06-Interview-Tips/02-estimation-cheatsheet.md',
'00-getting-started/study-plan.md':'01-Introduction/04-study-plan.md',
'01-foundations/03-networking-basics.md':'03-Concept-Deep-Dives/01-networking.md',
'02-core-concepts/03-caching.md':'03-Concept-Deep-Dives/02-caching.md',
'01-foundations/02-requirements-and-api-design.md':'03-Concept-Deep-Dives/03-api-design.md',
'02-core-concepts/04-database-fundamentals.md':'03-Concept-Deep-Dives/04-database-design.md',
'02-core-concepts/05-replication.md':'03-Concept-Deep-Dives/05-Distributed-Systems/01-replication.md',
'02-core-concepts/06-sharding-partitioning.md':'03-Concept-Deep-Dives/05-Distributed-Systems/02-sharding-partitioning.md',
'02-core-concepts/07-consistency-and-cap.md':'03-Concept-Deep-Dives/05-Distributed-Systems/03-consistency-and-cap.md',
'02-core-concepts/08-consistent-hashing.md':'03-Concept-Deep-Dives/05-Distributed-Systems/04-consistent-hashing.md',
# technologies
'03-technologies/03-relational-databases.md':'04-Technology-Deep-Dives/01-postgresql.md',
'03-technologies/01-redis.md':'04-Technology-Deep-Dives/03-redis.md',
'03-technologies/05-elasticsearch.md':'04-Technology-Deep-Dives/06-elasticsearch.md',
'03-technologies/02-kafka.md':'04-Technology-Deep-Dives/07-kafka.md',
'03-technologies/06-coordination-and-misc.md':'04-Technology-Deep-Dives/12-zookeeper.md',
# patterns
'02-core-concepts/11-resilience-and-failure-handling.md':'05-Interview-Patterns/09-surviving-component-failures.md',
'04-patterns/01-idempotency.md':'05-Interview-Patterns/10-preventing-duplicate-processing.md',
'04-patterns/02-saga.md':'05-Interview-Patterns/12-coordinating-transactions-across-services.md',
# reference
'02-core-concepts/01-scalability.md':'_Reference/scalability.md',
'02-core-concepts/02-load-balancing.md':'_Reference/load-balancing.md',
'02-core-concepts/09-messaging-and-streaming.md':'_Reference/messaging-and-streaming.md',
'02-core-concepts/10-rate-limiting.md':'_Reference/rate-limiting.md',
'02-core-concepts/12-cdn-and-storage.md':'_Reference/cdn-and-storage.md',
'02-core-concepts/13-microservices-and-communication.md':'_Reference/microservices-and-communication.md',
'02-core-concepts/14-security-basics.md':'_Reference/security-basics.md',
'02-core-concepts/15-search-and-geospatial.md':'_Reference/search-and-geospatial.md',
'03-technologies/04-nosql-stores.md':'_Reference/nosql-stores-overview.md',
'04-patterns/03-cqrs-event-sourcing.md':'_Reference/cqrs-event-sourcing.md',
'04-patterns/04-fanout-and-hot-keys.md':'_Reference/fanout-and-hot-keys.md',
'04-patterns/05-realtime-and-sync-patterns.md':'_Reference/realtime-and-sync-patterns.md',
'06-interview-questions/01-concept-qa.md':'_Reference/interview-questions/01-concept-qa.md',
'06-interview-questions/03-rapid-fire.md':'_Reference/interview-questions/02-rapid-fire.md',
'06-interview-questions/04-mock-interview-rubric.md':'_Reference/interview-questions/03-mock-interview-rubric.md',
}
inv={v:k for k,v in moves.items()}
allmd=[f for f in glob.glob('**/*.md',recursive=True)]
# resolve links & rewrite BEFORE moving (content edits in place at old path)
def fix(path):
    old=path; new=moves.get(path,path)
    s=open(old).read()
    def rep(m):
        t=m.group(2)
        if t.startswith(('http','mailto','#')): return m.group(0)
        pth,anc=(t.split('#',1)+[''])[:2] if '#' in t else (t,'')
        tgt=os.path.normpath(os.path.join(os.path.dirname(old),pth))
        tgt2=moves.get(tgt,tgt)
        r=os.path.relpath(tgt2,os.path.dirname(new))
        return m.group(1)+r+('#'+anc if anc else '')+m.group(3)
    s=re.sub(r'(\]\()([^)\s]+)(\))',rep,s)
    open(old,'w').write(s)
for f in allmd: fix(f)
for old,new in moves.items():
    os.makedirs(os.path.dirname(new),exist_ok=True)
    subprocess.check_call(['git','mv',old,new])
