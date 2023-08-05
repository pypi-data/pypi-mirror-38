import datetime as dt


def makedate(line):
    if len([d for d in line if d in '0123456789']) == 8:
        return dt.date(int(line[:4]),int(line[4:6]),int(line[6:]))

class TagsFilters(object):
    
    mdjpp_skip_notag_content = False
    mdjpp_skip_global_tag_content = False
    
    mdjpp_date_from = ""
    mdjpp_date_to = ""
    
    mdjpp_date_skip_notags = False
    mdjpp_date_skip_empty = False
    
    mdjpp_skip_tag = ""
    mdjpp_only_tag = ""
    mdjpp_only_global_tag = ""

class mdJPP(TagsFilters):
    pass
    

    def reparse_options(self):
        
        # date
        if self.mdjpp_date_from:
            self.mdjpp_date_from = makedate(self.mdjpp_date_from)
        if self.mdjpp_date_to:
            self.mdjpp_date_to = makedate(self.mdjpp_date_to)

    
default_options = mdJPP()

