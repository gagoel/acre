
var augment;

var Error = acreboot.Error;

(function() {

    augment = function (obj) {

        // augment the given object (normally the 'acre' object)
        
        obj.store = {
            "begin" : store.begin,
            "commit" : store.commit,
            "rollback" : store.rollback,
            "get" : get,
            "put" : put,
            "update" : update,
            "erase" : erase,
            "find" : find
        };

    };

    function get_appid() {
        var appid = acreboot._request_app_guid;
        if (!appid) throw Error("appid can't be null or undefined");
        return appid;
    }

    function get(id) {
        return store.get(get_appid(), id);
    }
    
    function put(obj) {
        return store.put(get_appid(), obj);
    }
    
    function update(id, obj) {
        return store.update(get_appid(), id, obj);
        
    }
    
    function erase(id) {
        var appid = get_appid();
        if (id instanceof Array) {
            for each (var i in id) {
                store.erase(appid, i);
            }
        } else {
            store.erase(appid, id);
        }
    }

    // ------------------- find ----------------------------

    function Result(result) {
        this.result = result;
    }
    
    Result.prototype.__iterator__ = function() {
        return new ResultIterator(this.result.as_iterator());
    };        

    function ResultIterator(iterator) {
        this.iterator = iterator;
    }

    ResultIterator.prototype.next = function() {
        if (this.iterator.has_next()) {
            return this.iterator.next();
        } else {
            throw StopIteration;
        }
    }
    
    function find(query) {
        var result = store.find(get_appid(), query);
        return new Result(result);
    }

})();
