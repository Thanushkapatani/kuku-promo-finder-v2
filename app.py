import streamlit as st
import zipfile, re, os, json, csv, io
from pathlib import Path
from modules.detector import analyze

st.set_page_config(page_title="Kuku Promo Finder V2", page_icon="🎬", layout="wide")
st.title("🎬 Kuku Promo Finder — Version 2")
st.caption("Dialogue-aware, event-aligned promo candidate ranking. Human editorial review required.")
uploaded=st.file_uploader("Upload the screenplay ZIP", type=["zip"])
if uploaded:
    results=[]; count=0
    with zipfile.ZipFile(uploaded) as z:
        names=[n for n in z.namelist() if n.lower().endswith(".txt")]
        for n in names:
            raw=z.read(n).decode("utf-8", errors="replace")
            results.extend(analyze(os.path.basename(n),raw)); count+=1
    results.sort(key=lambda x:x["score"], reverse=True)
    st.success(f"Processed {count} screenplay files; generated {len(results)} candidates.")
    if results:
        st.metric("Episodes represented",len(set(r["episode"] for r in results)))
        st.subheader("Top candidates")
        for i,r in enumerate(results[:20],1):
            with st.expander(f"#{i} · Episode {r['episode']} · {r['start_time']}–{r['end_time']} · {r['duration']}s · {r['score']}"):
                st.write("**Opening beat**",r["hook"])
                st.caption(f"Opening source: {r['hook_type']}")
                st.write("**Ending beat**",r["cliffhanger"])
                st.caption(f"Ending source: {r['ending_type']}")
                st.write("**Why selected**",r["why"])
                st.write("**Episode context**",r["logline"])
        st.download_button("Download JSON",json.dumps(results,indent=2,ensure_ascii=False),file_name="promo_candidates_v2.json",mime="application/json")
        buf=io.StringIO(); fields=list(results[0].keys()); w=csv.DictWriter(buf,fieldnames=fields);w.writeheader();w.writerows(results)
        st.download_button("Download CSV",buf.getvalue(),file_name="promo_candidates_v2.csv",mime="text/csv")
else:
    st.info("Upload the supplied ZIP containing episode TXT files.")
st.markdown("---")
st.markdown("**Version 2 method:** timestamped beats are classified using their screenplay section labels. Dialogue is preferred for hooks/endings, while visual/action beats remain eligible and are labelled. Candidates are aligned to beat start times, scored using opening/ending dialogue, tension terms, beat density and logline overlap, then filtered for heavy interval overlap. Scores are heuristic, not model-generated judgements.")
