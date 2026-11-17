# -*- coding: utf-8 -*-
"""Check tree shape and numbering. Semantic completeness requires source review."""
import io,re,sys
NODE=re.compile(r"^( *)(- (.*))$")
NUMBER=re.compile(r"^(\d+(?:\.\d+)*\.?)(?:\s+|(?=[^\d.]))")
def check(path):
 rows=[]; problems=[]
 for i,line in enumerate(io.open(path,encoding="utf-8").read().splitlines(),1):
  m=NODE.match(line)
  if m: rows.append({"line":i,"indent":len(m.group(1)),"text":m.group(3).strip()})
  elif line.strip(): rows.append({"line":i,"indent":-1,"text":line.strip()})
 nodes=[r for r in rows if r["indent"]>=0]; roots=[r for r in nodes if r["indent"]==0]
 if not nodes: problems.append("no tree nodes")
 if len(roots)!=1: problems.append("root count %d (expected 1)"%len(roots))
 for r in rows:
  if r["indent"]<0: problems.append("non-tree text L%d: %s"%(r["line"],r["text"][:50]))
  elif r["indent"]%2: problems.append("odd indentation L%d"%r["line"])
 parsed=[]
 for r in nodes:
  if r["indent"]==0: continue
  m=NUMBER.match(r["text"])
  if not m: problems.append("unnumbered node L%d: %s"%(r["line"],r["text"][:50])); continue
  label=m.group(1).rstrip("."); parts=tuple(int(x) for x in label.split('.')); depth=r["indent"]//2
  if len(parts)!=depth: problems.append("number/indent mismatch L%d: %s"%(r["line"],label))
  parsed.append((r,parts))
 seen={p for _,p in parsed}; previous={}
 for r,parts in parsed:
  parent=parts[:-1]
  if parent and parent not in seen: problems.append("orphan node L%d: missing parent %s"%(r["line"],'.'.join(map(str,parent))))
  if parent in previous and parts[-1]!=previous[parent]+1: problems.append("number gap L%d: %s"%(r["line"],'.'.join(map(str,parts))))
  previous[parent]=parts[-1]
 return {"tree_nodes":len(nodes),"roots":len(roots),"max_depth":max((r["indent"]//2+1 for r in nodes),default=0)},problems
if __name__=="__main__":
 stats,problems=check(sys.argv[1]); print(stats); print("PASS" if not problems else "\n".join(problems))
