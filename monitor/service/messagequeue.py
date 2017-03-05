from kombu import  Connection,Exchange,Queue
from kombu.pools import producers
from kombu.mixins import ConsumerMixin
import threading

from monitor.service.scheduler import SingletonMixin

class MessageManager(SingletonMixin):

    def __init__(self):
        self.media = Exchange("monitor", 'direct')
        self.queue_cache = {}
        self.connection = Connection('memory:///')

    def create_binding_queue(self, id):
        if not self.queue_cache.has_key(id):
            self.queue_cache[id] = Queue(id, exchange=self.media, routing_key=id)
        return self.queue_cache[id]



class MessageSender(object):
    @staticmethod
    def send_msg(topic,payload):
        with producers[MessageManager.instance().connection].acquire(block=True) as producer:
            producer.publish(payload,
                         serializer='json',
                         exchange=MessageManager.instance().media,
                         declare=[MessageManager.instance().media],
                         routing_key=topic)


'''
   Each comsumer is a single thread
'''
class BaseConsumer(ConsumerMixin, threading.Thread):

    def __init__(self, routing_key):
        super(BaseConsumer,self).__init__()
        self.connection = MessageManager.instance().connection
        self.routing_key = routing_key
        self.maintainence_flag = False

    def get_consumers(self, Consumer, channel):
        return [
            Consumer([Queue(self.routing_key, exchange=MessageManager.instance().media,
                        routing_key=self.routing_key)], callbacks=[self.msg_handler],
                        accept=['json']),
        ]

    def msg_handler(self, body, message):
        if not self.maintainence_flag:
            self.on_message(body, message)

    def set_maintainence(self):
        self.maintainence_flag = True

    def clear_maintainence(self):
        self.maintainence_flag = False

    def on_message(self, body, message):
        raise NotImplementedError('Subclass responsibility')


class SampleConsumer(BaseConsumer):
    def __init__(self, name):
        super(SampleConsumer,self).__init__(name)
        self.name = name

    def on_message(self, body, message):
        try:
            eventName = body["eventName"]
            if eventName:
                methodName = "handle%s" % eventName
                if hasattr(self, methodName):
                    method = getattr(self, methodName)
                    method(body)

            message.ack()
        except Exception,e:
            pass

    def handleTerminateProgram(self,body):
        import thread,os
        print "handleTestAction was call with %s" % body
        print "Consumer :%s @ %s" % (thread.get_ident(), os.getegid())
        os._exit(0)


if __name__ == '__main__':
    import time,thread,os
    route_key = "test"
    SampleConsumer(route_key).start()
    time.sleep(10)
    MessageSender.send_msg(route_key, {"eventName": "TerminateProgram" ,"transferValue": "Hello World"})

    print "start looping..."

    while True:
        print "Main :%s @ %s" % (thread.get_ident(), os.getegid())
        time.sleep(10)
