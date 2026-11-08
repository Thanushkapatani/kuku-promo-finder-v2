    if not inside:return None
    opening=[e for e in inside if e["start"]<=start+8 and e["end"]>=start]
    ending=[e for e in inside if e["end"]>=end-9]
    od=[e for e in opening if e["kind"]=="dialogue" and e["dialogue"]]
    ed=[e for e in ending if e["kind"]=="dialogue" and e["dialogue"]]
    text=" ".join(e["dialogue"] or e["text"] for e in inside).lower()
    terms=["betray","marry","murder","kill","secret","truth","never","why","no","stop","help","dead","pregnant","revenge","threat","leave","choose","prove","swear","unless","cannot","can't","hate","love","father","sister"]
    tension=sum(1 for word in terms if word in text)
    clarity=sum(1 for word in re.findall(r"[A-Za-z']+",logline.lower()) if len(word)>4 and word in text)
    score=round((5 if od else 1.5)+(4 if ed else 1)+min(tension,10)*.65+min(len(inside),15)*.18+min(clarity,5)*.35,2)
    hook=od[0]["dialogue"] if od else (opening[0]["text"] if opening else inside[0]["text"])
    cliff=ed[-1]["dialogue"] if ed else (ending[-1]["text"] if ending else inside[-1]["text"])
    return {"start":start,"end":end,"duration":round(end-start,2),"score":score,"hook":hook[:250],"cliffhanger":cliff[:250],
            "hook_type":"dialogue" if od else "visual/action","ending_type":"dialogue" if ed else "visual/action",
            "dialogue_beats":sum(e["kind"]=="dialogue" for e in inside),
            "why":f"{len(inside)} timed beats; {sum(e['kind']=='dialogue' for e in inside)} dialogue beats; {tension} tension signals; {len(od)} opening dialogue beat(s); {len(ed)} ending dialogue beat(s)."}

def analyze(filename,raw):
    events=extract_events(raw)
    if not events:return []
    match=re.search(r"EPISODE LOGLINE:\s*(.*)",raw)
    logline=match.group(1).strip() if match else ""
    last=max(e["end"] for e in events); candidates=[]
    for start in sorted(set(e["start"] for e in events)):
        for duration in (25,30,35,40,45,50,55,60):
            end=start+duration
            if end<=last:
                result=evaluate(events,start,end,logline)
                if result:candidates.append(result)
    candidates.sort(key=lambda x:x["score"],reverse=True)
    selected=[]
    for c in candidates:
        overlaps=False
        for s in selected:
            overlap=max(0,min(c["end"],s["end"])-max(c["start"],s["start"]))
            if overlap/max(1,min(c["duration"],s["duration"]))>=.25:
                overlaps=True;break
        if not overlaps:selected.append(c)
        if len(selected)==3:break
    match=re.search(r"episode-(\d+)",filename,re.I); ep=int(match.group(1)) if match else 0
    for rank,c in enumerate(selected,1):
        # Round the displayed start once, then derive the displayed end from
        # that rounded start plus the candidate duration. This keeps the
        # visible timestamps consistent with the displayed duration.
        display_start = int(round(c["start"]))
        display_duration = int(round(c["duration"]))
        c.update({
            "episode": ep,
            "rank_in_episode": rank,
            "start_time": stamp(display_start),
            "end_time": stamp(display_start + display_duration),
            "logline": logline
        })
        c.pop("start", None)
        c.pop("end", None)
    return selected
