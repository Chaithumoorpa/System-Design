import os,re,sys
sys.path.insert(0,os.path.dirname(__file__))
from roadmap import *
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..')); os.chdir(R)
def rel(a,b): return os.path.relpath(b,os.path.dirname(a))
items=[]  # (path,title,prio,diff,section_title,section_folder)
for sec in SECTIONS:
    for it in sec[3]: items.append((item_path(sec,it),it[1],it[2],it[3],sec[1],sec[0]))
seq=[i for i in items if os.path.exists(i[0])]
def status(p): return '✅' if os.path.exists(p) else '🚧'
CRED=("> 📚 **Credit:** Chapter selection, ordering and question choice follow the "
      "[AlgoMaster.io System Design Interviews course]({url}). This write-up was created with Claude "
      "for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS]({credits}).")
def block(path,idx):
    p,title,pr,df,st,sf=seq[idx]
    prev=seq[idx-1] if idx>0 else None; nxt=seq[idx+1] if idx+1<len(seq) else None
    parts=[]
    parts.append(f"⬅️ Previous: [{prev[1]}]({rel(p,prev[0])})" if prev else "⬅️ Previous: *(start)*")
    parts.append(f"🏠 [{st}]({rel(p,sf+'/README.md')})")
    parts.append(f"➡️ Next: [{nxt[1]}]({rel(p,nxt[0])})" if nxt else "➡️ Next: *(end)*")
    tag=f"🏷️ **Priority:** {pr} · **Difficulty:** {df}\n\n" if pr else ""
    return ("<!-- nav:start -->\n"+tag+" · ".join(parts)+"\n\n"+CRED.format(url=ROADMAP_URL,credits=rel(p,'CREDITS.md'))+"\n<!-- nav:end -->")
for idx,(p,*_) in enumerate(seq):
    s=open(p).read()
    s=re.sub(r'<!-- nav:start -->.*?<!-- nav:end -->\n?','',s,flags=re.S)
    s=re.sub(r'^> 📚 \*\*Credit:\*\*.*?\n(?:>.*\n)*\n?','',s,flags=re.M)
    s=re.sub(r'^⬅️ Previous:.*\n\n?','',s,flags=re.M)
    lines=s.split('\n'); 
    for i,l in enumerate(lines):
        if l.startswith('# '): break
    lines.insert(i+1,'\n'+block(p,idx)+'\n')
    open(p,'w').write(re.sub(r'\n{3,}','\n\n','\n'.join(lines)))
# section READMEs
for sec in SECTIONS:
    folder,title,kind,its=sec
    rows=[]
    for n,it in enumerate(its,1):
        p=item_path(sec,it)
        rows.append(f"| {n} | [{it[1]}]({rel(folder+'/README.md',p)}) | {it[2] or '—'} | {it[3] or '—'} | {status(p)} |")
    done=sum(1 for it in its if os.path.exists(item_path(sec,it)))
    os.makedirs(folder,exist_ok=True)
    open(folder+'/README.md','w').write(f"# {title}\n\n{done}/{len(its)} chapters written.\n\n| # | Chapter | Priority | Difficulty | Status |\n|---|---|---|---|---|\n"+"\n".join(rows)+
      f"\n\n> Chapter selection and tags credited to the [AlgoMaster.io course roadmap]({ROADMAP_URL}). Content written with Claude. See [CREDITS](../CREDITS.md).\n\n⬅️ [Course roadmap](../README.md)\n")
# root README
tot=sum(len(s[3]) for s in SECTIONS if s[0]!='01-Introduction' or True); done=sum(1 for i in items if os.path.exists(i[0]))
out=[f"""# 🏗️ System Design Interviews — Study Guide

Study material, deep dives and worked interview questions for **system design rounds at product-based
companies**, organised as a course. Every problem follows the same flow:
**Clarify → Estimate → Core APIs → High-Level Design → Database Design → Deep Dive → Follow-ups (answered) → Practice → Revision**.

> 📚 **Credit:** The course outline (chapter selection, order, and priority/difficulty tags) and the
> choice of interview questions are credited to
> [AlgoMaster.io — System Design Interviews]({ROADMAP_URL}).
> All text, numbers, tables and diagrams in this repository were written with Claude for personal
> interview preparation; the premium lesson content was **not** accessed or reproduced.
> Not affiliated with AlgoMaster.io: please support the original at [algomaster.io](https://algomaster.io).
> See [CREDITS.md](CREDITS.md).

**Progress: {done}/{len(items)} chapters written.** ✅ written · 🚧 planned

## How to study

1. Start with [Introduction](01-Introduction/README.md) and the [study plan](01-Introduction/04-study-plan.md).
2. Learn the **Must-Know Topics**, **Concept** and **Technology** deep dives.
3. Learn the **Interview Patterns** (reusable solutions to recurring problems).
4. Practise the **Design Questions**: read only the prompt, attempt it for 35 minutes, then compare.
5. Use [`_Reference/`](_Reference/README.md) for quick-revision Q&A, rapid-fire drills and the mock-interview rubric.

Priority = how often the topic appears in interviews; difficulty = how hard it is to learn.
Tools: `python3 tools/build.py` regenerates navigation, indexes and this table.
"""]
for sec in SECTIONS:
    folder,title,kind,its=sec
    out.append(f"\n## [{title}]({folder}/README.md)\n\n| Chapter | Priority | Difficulty | Status |\n|---|---|---|---|")
    for it in its:
        p=item_path(sec,it); out.append(f"| [{it[1]}]({p}) | {it[2] or '—'} | {it[3] or '—'} | {status(p)} |")
out.append("\n## 🔗 Companion repository\n\nObject-oriented (low-level) design: [Low-Level-Design](https://github.com/Chaithumoorpa/Low-Level-Design).\n")
open('README.md','w').write("\n".join(out))
print('written',done,'of',len(items))
