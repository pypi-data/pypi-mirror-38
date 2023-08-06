from intervaltree import Interval,IntervalTree
class IntervalNewTree(IntervalTree):
    def __init__(self,*args,**kwargs):
        IntervalTree.__init__(self,*args,**kwargs)
    def length(self):
        return sum([i.length() for i in self])
    def merge_intrv(self,intrv):
        out = IntervalNewTree()
        targets = self[intrv.begin:intrv.end]
        for iv in targets:
            out.addi(max(intrv.begin,iv.begin),min(intrv.end,iv.end))
        return out      
    @staticmethod
    def merge_tree(tree1,tree2): 
        out = []
        # if len(tree2) < len(tree1):tree1,tree2 = tree2,tree1        
        for intrv in tree1:
            targets = sorted(tree2[intrv.begin:intrv.end])
            if len(targets) == 0:
                continue
            elif len(targets) == 1:
                out.append(Interval(max(intrv[0],targets[0][0]),min(intrv[1],targets[0][1])))
            else:
                out.extend([Interval(max(intrv[0],targets[0][0]),targets[0][1]),Interval(targets[-1][0],min(intrv[1],targets[-1][1]))] + targets[1:-1])
        return IntervalNewTree(out)      
    def split_tree(self,between=1):
        if len(self) == 0:return
        intrvlist = sorted(self.items())
        out = [IntervalNewTree([Interval(intrvlist[0].begin,intrvlist[0].end)]),]
        for i in range(1,len(intrvlist)):
            if intrvlist[i].distance_to(intrvlist[i-1]) <= between:
                out[-1].add(intrvlist[i])
            else:
                out.append(IntervalNewTree([Interval(intrvlist[i].begin,intrvlist[i].end)]))        
        return out
    def range_tree(self):  
        return (j for i in self for j in range(i.begin,i.end))
    @classmethod
    def from_tuples(cls, tups):
        ivs = [Interval(*t) for t in tups]
        return IntervalNewTree(ivs)
    def merge_overlaps2(self,between=0):
        self.merge_overlaps()
        if len(self) <= 1 or between == 0:return self
        ivs = sorted(self)
        out = [[ivs[0][0],ivs[0][1]],]
        for iv in ivs[1:]:
            if iv[0] <= out[-1][-1]+between:
                out[-1][-1] = iv[1]
            else:
                out.append([iv[0],iv[1]])
        return IntervalNewTree.from_tuples(out)
    def __repr__(self):
        if self:
            return "IntervalNewTree({0})".format(sorted(self))
        return "IntervalNewTree()"
    __str__ = __repr__  
