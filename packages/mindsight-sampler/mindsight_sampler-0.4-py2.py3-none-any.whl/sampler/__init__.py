import json
import requests, requests.exceptions
import signal


s = None


def start(server_url, project, modules, environment=None, interval=0.01, send_after=1000):
    global s
    if s is not None:
        s._enabled = True
        s.start()
        return

    s = Sampler(server_url, project, modules, environment=environment, interval=interval, send_after=send_after)
    s.start()


def stop():
    global s
    s.stop()


class Sampler(object):
    def __init__(self, server_url, project, modules, environment=None, interval=0.01, send_after=1000):
        self.server_url = server_url
        self.project = project
        self.modules = tuple(modules)
        self.environment = environment
        self.interval = interval
        self.send_after = send_after
        self._samples = {}
        self._count = 0
        self._enabled = True
        self.url = "{}/samples/?project={}".format(server_url, project)
        if environment is not None:
            self.url += "&environment={}".format(environment)


    def _sample(self, signum, frame):
        if not self._enabled:
            return

        while frame is not None:
            formatted_frame = '{}.{}'.format(frame.f_globals.get('__name__'),
                frame.f_code.co_name)
            
            if formatted_frame.startswith(self.modules):
                if formatted_frame not in self._samples:
                    self._samples[formatted_frame] = 1
                else:
                    self._samples[formatted_frame] += 1
                break

            frame = frame.f_back

        self._count += 1

        if self._count >= self.send_after:
            self._count = 0
            self._send_samples()

        signal.setitimer(signal.ITIMER_VIRTUAL, self.interval, 0)


    def _send_samples(self):
        if len(self._samples) == 0:
            return

        try:
            h = {"Content-type": "application/json"}
            data = json.dumps(self._samples)
            r = requests.post(self.url, headers=h, data=data, timeout=0.01)
            r.raise_for_status()
            self._samples = {}
        except requests.exceptions.RequestException as e:
            print(e)


    def start(self):
        signal.signal(signal.SIGVTALRM, self._sample)
        signal.setitimer(signal.ITIMER_VIRTUAL, self.interval, 0)


    def stop(self):
        self._enabled = False
