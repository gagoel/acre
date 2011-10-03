from acre_py_tests import *
import re
import urllib2
try:
    import simplejson
except ImportError:
    import json as simplejson
from unittest import TestCase

class test_class(TestController):
    @tag(bug=False, bugid="ACRE-202", slow=True)
    def test_urlfetch_returns_error_200_204(self):
        try:
            r = range(200,204)
            for code in r:
                url = "%s/return_status?status=%s" % (self.host, code);
                print "target url: %s" % url;
                self.set_acre_script("urlfetch_error", { "url": url })
                self.get();
                response = self.response.read();
                print "Got response %r" % response;
                response = simplejson.loads(response);
                message = response['message'];
                print "Got message: %s" % message;

                expected_message = "no exception thrown"
                p = re.compile(expected_message);
                self.assert_( p.match(message), "urlfetch returned an unexpected message.  Expected:\n%s\nGot:\n%s\n" %(expected_message, message));
        except urllib2.HTTPError, e:
            print(self.log);
            self.assert_(False, "Got unexpected http error. %s" % e);
 
        except Exception, e:
            self.assert_(False, "test threw unexpected error. %s" % e);

    #@tag(bug=True, bugid="ACRE-1493", oldbugs=["ACRE-202"], slow=True)
    #def test_urlfetch_returns_error_205(self):

    @tag(bug=False, bugid="ACRE-204", slow=True)
    def test_urlfetch_returns_error_206(self):
        try: 
            r = range(206,207)
            for code in r:
                url = "%s/return_status?status=%s" % (self.host, code);
                print "target url: %s" % url;
                self.set_acre_script("urlfetch_error", { "url": url })
                self.get();
                response = self.response.read();
                print "Got response %s" % response;
                response = simplejson.loads(response);
                message = response['message'];
                print "Got message: %s" % message;
                expected_message = "no exception thrown"
                p = re.compile(expected_message);
                self.assert_( p.match(message), "urlfetch returned an unexpected message.  Expected:\n%s\nGot:\n%s\n" %(expected_message, message));
        except urllib2.HTTPError, e:
            print(self.log);
            self.assert_(False, "Got unexpected http error. %s" % e);
 
        except Exception, e:
            self.assert_(False, "test threw unexpected error. %s" % e);

    @tag(bug=False, bugid="ACRE-202", slow=True) 
    def test_urlfetch_returns_error_207_210(self):
        try: 
            r = range(207,210);
            for code in r:
                url = "%s/return_status?status=%s" % (self.host, code);
                print "target url: %s" % url;
                self.set_acre_script("urlfetch_error",  { "url": url })
                self.get();
                response = self.response.read();
                print "Got response %s" % response;
                response = simplejson.loads(response);
                message = response['message'];
                print "Got message: %s" % message;
                expected_message = "no exception thrown"
                p = re.compile(expected_message);
                self.assert_( p.match(message), "urlfetch returned an unexpected message.  Expected:\n%s\nGot:\n%s\n" %(expected_message, message));
        except urllib2.HTTPError, e:
            print(self.log);
            self.assert_(False, "Got unexpected http error. %s" % e);
 
        except Exception, e:
            self.assert_(False, "test threw unexpected error. %s" % e);

    @tag(login=True)
    def test_urlfetch_returns_error_305_307(self):
        try:
            #self.login();
            r = range(305,307)
            for code in r:
                #self.touch(); 
                url = "%s/return_status?status=%s" % (self.host, code);
                print "target url: %s" % url;
                self.set_acre_script("urlfetch_error", { "url": url })

                expected_message = "urlfetch failed: %s" % code;
                msg_pattern = re.compile(expected_message);

                expected_body = "status is: %s" % code;
                body_pattern = re.compile(expected_body);

                self.get();
                response = self.response.read();
                response = simplejson.loads(response);
                print "Got response %s" % response;

                message = response['message'];
                print "Got message: %s" % message;

                self.assert_( msg_pattern.search(message), "urlfetch returned an unexpected message.  Expected:\n%s\nGot:\n%s\n" %(expected_message, message));

                body = response['response']['body'];
                print "Got body: %s" % body;

                self.assert_( body_pattern.search(body), "urlfetch returned an unexpected body.  Expected:\n%s\nGot:\n%s\n" % (expected_body, body));
        
        except urllib2.HTTPError, e:
            # print(self.log);
            self.assert_(False, "Got unexpected http error. %s" % e);
 
        except Exception, e:
            self.assert_(False, "test threw unexpected error. %s" % e);

    #@tag(bug=True, oldbugs=["ACRE-205", "ACRE-1157"], bugid="ACRE-1494", slow=True)
    #def test_urlfetch_returns_error_400_500(self):

    @tag(bug=False, bugid="ACRE-1114")
    def test_urlfetch_error_no_protocol(self):
        self.set_acre_script( "urlfetch_error" );
	self.data = self.encode_data( { "url": "www.google.com" } );
	try: 
	    self.get();
	    response = self.response.read();
	    response_json = simplejson.loads(response)
	    self.assert_( response_json['message'] == "Malformed URL: www.google.com", "Got unexpected response: %s" % response_json );
	except HTTPError, e:
	    body = e.fp.read();
	    print "Got error: %s\n%s" % (e.code, body);

test_class.reviewed = True