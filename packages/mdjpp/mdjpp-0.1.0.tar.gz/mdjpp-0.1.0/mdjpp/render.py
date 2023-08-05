import hashlib
from functools import wraps

from mdjpp.tags import Multi, Date

def auto_color(value):
    return hashlib.md5(value.encode('utf-8')).hexdigest()[:6]

class sstr(str):
    pass

def ensure_sstr(gen):
    @wraps(gen)
    def patched(*args, **kwargs):
        return sstr(gen(*args, **kwargs))
    return patched


class Engine(object):
        
    def hrme(self,line):
        return """
---

%s

---
""" % str(line)


    def tag_opener(self,tag):
        raise NotImplementedError("Method not implemented")
        
    def tag_closer(self,tag):
        raise NotImplementedError("Method not implemented")
    
    @ensure_sstr
    def tag(self,tag):
        if isinstance(tag,Date):
            return self.tag_date(tag)
        elif isinstance(tag,Multi):
            return self.tag_multi(tag)
    
    def tag_date(self,tag):
        raise NotImplementedError("Method not implemented")
        
    def tag_verbatim(self,tag):
        raise NotImplementedError("Method not implemented")
        
    def tag_multi(self,tag):
        raise NotImplementedError("Method not implemented")
    


class HTML(Engine):
    
    @ensure_sstr
    def tag_opener(self,tag):
        #return """<div style="margin:20px; border:1px solid black;">"""
        #return """<div style="margin:20px;">"""
        return """<div style="margin:1px;">"""
        
    @ensure_sstr
    def tag_closer(self,tag):
        return """</div>"""
        
    @ensure_sstr
    def tag_date(self,tag):
        return self.hrme("""<p><strong>%s</strong></p>""" % str(tag.value))
        
    @ensure_sstr
    def tag_verbatim(self,tag):
        color = auto_color(tag.value)
        return """<span style="border:1px solid black; color:#%s">%s</span>""" % (color,str(tag.value))
        
    @ensure_sstr
    def tag_multi(self,tag):
        return """<p>%s</p>""" % ' '.join(map(self.tag_verbatim,tag.value))
    
