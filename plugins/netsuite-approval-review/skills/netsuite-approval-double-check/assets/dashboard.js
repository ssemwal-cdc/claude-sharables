// Dashboard code for the netsuite-approval-review dashboard. The shell, dashboard_template.html, holds the markup, the
// data block and the guard; publish_dashboard.py either inlines this file or leaves a pinned CDN tag.
var ACCT="";
// Only `account` is used here, to build record URLs. `me` and `tool` stay in the payload as a
// record of which route produced the review, but the page has no use for them.
ACCT=(REVIEW.config&&REVIEW.config.account)||"";

// Mark keys, kept named although nothing writes them. The per-item marks lived in
// localStorage under `ns_marks_v1`, each entry {kind:"approve"|"notes"|"reject", text:""}.
// Never rename or reuse that key: an old browser still holds real decisions under it.
// D38, never rename a marks key; retired by review-only-mode.

// ---- view state: sort / filter / search, persisted ---------------------------
// A NEW key beside ns_marks_v1, never a rename of it. Marks were decisions the user had
// made; a view is just what they are looking at. Losing the second
// costs a scroll, losing the first silently discards real work.
// v2 because the default sort changed. A stored v1 view would otherwise pin everyone who
// has ever touched the toolbar to the old default for good, and the change would reach
// nobody who already uses the page - which is everybody it is for. The migration carries
// their filters and search across and resets only the sort, so the cost is not even a scroll.
var VKEY="ns_view_v2", OLDVKEY="ns_view_v1";
var DEFV={sort:"newest",type:"all",vendor:"all",q:""};
//__SHARED:dash-view-migration__
var view=Object.assign({},DEFV);
try{
  var sv=JSON.parse(localStorage.getItem(VKEY)||"null");
  if(!sv){var old=JSON.parse(localStorage.getItem(OLDVKEY)||"null");
          if(old){sv=Object.assign({},old); delete sv.sort}}
  if(sv)view=Object.assign(view,sv);
}catch(e){}
function saveView(){try{localStorage.setItem(VKEY,JSON.stringify(view))}catch(e){}}
//__END_SHARED:dash-view-migration__
function setView(k,v){
  view[k]=v; saveView(); render();
  if(k==="q"){var e=document.getElementById("fQ"); if(e){e.focus(); e.setSelectionRange(e.value.length,e.value.length)}}
}
function resetView(){view=Object.assign({},DEFV);saveView();render()}
function viewActive(){return view.type!=="all"||view.vendor!=="all"||!!view.q}

// Takes the {it,c} wrappers render() builds rather than bare items: c.state carries the
// verdict as classified against the live queue, which is what the verdict sort orders on.
function applyView(list){
  var q=(view.q||"").toLowerCase().trim();
  var out=list.filter(function(r){
    var i=r.it;
    if(view.type!=="all"   && i.type!==view.type)return false;
    if(view.vendor!=="all" && i.vendor!==view.vendor)return false;
    if(q){
      var hay=(i.doc+" "+i.vendor+" "+i.type+" "+(i.id||"")+" "+i.head).toLowerCase();
      if(hay.indexOf(q)<0)return false;
    }
    return true;
  });
  var s=view.sort;
  out.sort(function(a,b){
    var ai=a.it, bi=b.it;
    var ad=ageDaysRaw(ai.trandate), bd=ageDaysRaw(bi.trandate);
    //__SHARED:dash-date-comparator__
    // Both-null has to return 0. The previous shape returned 1 for both orderings, which is
    // not a valid comparator and lets an engine produce an arbitrary order from it.
    function bydate(oldestFirst){
      if(ad==null&&bd==null)return 0;
      if(ad==null)return 1;
      if(bd==null)return -1;
      return oldestFirst?bd-ad:ad-bd;
    }
    //__END_SHARED:dash-date-comparator__
    switch(s){
      case "oldest":  return bydate(true) || (ai.id||0)-(bi.id||0);
      case "amtDesc": return (bi.amt||0)-(ai.amt||0);
      case "amtAsc":  return (ai.amt||0)-(bi.amt||0);
      case "vendor":  return String(ai.vendor).localeCompare(String(bi.vendor),undefined,{numeric:true}) ||
                             (bi.amt||0)-(ai.amt||0);
      // Still available, just no longer the default. Flagged first, then history open, then clear, each tier
      // by amount descending.
      case "verdict": var o={flagged:0,"history-open":1,clear:2};
                      return (o[a.c.state]-o[b.c.state]) || (bi.amt||0)-(ai.amt||0);
      // Newest is the default now. trandate is day-granular, so same-day bills would fall
      // back to whatever order publish_dashboard.py pre-sorted them into; the internal id
      // descending breaks that tie by arrival, the closest thing NetSuite gives to "latest".
      default:        return bydate(false) || (bi.id||0)-(ai.id||0);
    }
  });
  return out;
}

function fillFilters(rows){
  function counts(arr,key){var o={};arr.forEach(function(r){var v=r.it[key];o[v]=(o[v]||0)+1});return o}
  function opts(vals,cts,cur){
    return '<option value="all">All</option>'+vals.map(function(v){
      return '<option value="'+esc(v)+'"'+(v===cur?' selected':'')+'>'+esc(v)+' ('+cts[v]+')</option>'}).join("");
  }
  var types=[]; rows.forEach(function(r){if(types.indexOf(r.it.type)<0)types.push(r.it.type)}); types.sort();
  var tSel=document.getElementById("fType");
  tSel.innerHTML=opts(types,counts(rows,"type"),view.type);
  if(types.indexOf(view.type)<0 && view.type!=="all"){view.type="all";tSel.value="all"}

  // Vendor list narrows to the chosen type, the way Procore's buildings narrow to campus.
  var scope = view.type==="all" ? rows : rows.filter(function(r){return r.it.type===view.type});
  var vends=[]; scope.forEach(function(r){if(vends.indexOf(r.it.vendor)<0)vends.push(r.it.vendor)});
  vends.sort(function(a,b){return String(a).localeCompare(String(b),undefined,{numeric:true})});
  var vSel=document.getElementById("fVendor");
  vSel.innerHTML=opts(vends,counts(scope,"vendor"),view.vendor);
  if(vends.indexOf(view.vendor)<0 && view.vendor!=="all"){view.vendor="all";vSel.value="all"}

  document.getElementById("fSort").value=view.sort;
  var qEl=document.getElementById("fQ"); if(qEl.value!==view.q)qEl.value=view.q;
  tSel.className=view.type!=="all"?"act":"";
  vSel.className=view.vendor!=="all"?"act":"";
  document.getElementById("fReset").className="chip"+(viewActive()||view.sort!==DEFV.sort?" on":"");
}

var money=function(n){return Math.abs(n).toLocaleString("en-US",{style:"currency",currency:"USD",minimumFractionDigits:2})};
// Rolls over into millions. The card used to inline total/1000 with no rollover, so a $2.7m
// queue rendered as "$2702k". Same helper as the Procore template.
//__SHARED:dash-compact-money__
function compactMoney(n){
  n=Math.abs(n||0);
  if(n<1000)return "$"+Math.round(n);
  var k=Math.round(n/1000);
  if(k>=1000)return "$"+(Math.round(n/1e5)/10)+"m";
  return "$"+k.toLocaleString()+"k";
}
//__END_SHARED:dash-compact-money__
function parseNsDate(s){if(!s)return null;var p=String(s).split("/");if(p.length!==3)return null;return new Date(+p[2],+p[0]-1,+p[1])}
// Two of these on purpose. ageDays clamps at zero because "-3 days pending" is nonsense to
// read; ageDaysRaw does not, because that clamp collapses every future-dated bill to 0, so
// they tie with each other and with today's. Invisible under the old verdict default and
// wrong at the top of a newest-first list. Display uses the clamp, the comparator does not.
function ageDaysRaw(s){var d=parseNsDate(s);if(!d)return null;return Math.floor((Date.now()-d.getTime())/86400000)}
function ageDays(s){var a=ageDaysRaw(s);return a==null?null:Math.max(0,a)}
function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}
//__SHARED:dash-nav__
function nav(a){
  // The widget host exposes openLink as a bare global; target=_blank is unreliable in a sandboxed
  // iframe. Fall through to the anchor on any host that does not provide it.
  if(window.openLink){try{window.openLink(a.href);return false}catch(e){}}
  return true
}
//__END_SHARED:dash-nav__
function recUrl(id){return "https://"+ACCT+".app.netsuite.com/app/accounting/transactions/transaction.nl?id="+id}

// This page never queries NetSuite. The widget host exposes no callMcpTool, and an on-open
// query would be stale by the time anyone read it anyway.
// So every row is a snapshot reading, which is what `stale` below records. A `live` queue
// variable and the gone/changed/unreviewed states it fed were carried here unassigned for
// several versions - dead in every render. Removed; do not reintroduce an on-open query.

function ageOfRun(){var t=new Date(REVIEW.lastRunISO).getTime();if(isNaN(t))return null;return Math.max(0,Math.round((Date.now()-t)/60000))}
function ageText(){var m=ageOfRun();if(m==null)return "";
  if(m<2)return "just now"; if(m<60)return m+" minutes ago";
  var h=Math.round(m/60); if(h<24)return h+" hour"+(h>1?"s":"")+" ago";
  var d=Math.round(h/24); return d+" day"+(d>1?"s":"")+" ago";}

function classify(it){return{state:it.verdict,stale:true}}

var STALE_NOTE=" — this snapshot is getting old. NetSuite may have moved on; re-run before acting on anything below.";
// Split out of render() so the 60s tick can age this without rebuilding the queue.
function freshTick(){
  var stale=isStale();
  var ft=document.getElementById("freshtext");
  ft.className="fresh"+(stale?" stale":"");
  ft.innerHTML='Reviewed '+ageText()+' · '+esc(REVIEW.lastRun)+(stale?STALE_NOTE:'');
  var conn=document.getElementById("conn");
  conn.textContent=stale?"Snapshot · "+ageText():"Snapshot · fresh";
  conn.style.background=stale?"var(--bad-bg)":"var(--ok-bg)";
  conn.style.color=stale?"var(--bad-fg)":"var(--ok-fg)";
}
function isStale(){var m=ageOfRun();return m!=null&&m>180}
// A clamped warning offers `more` only when three lines actually clip something.
// Emitted unconditionally, a one-line warning got a control that did nothing.
function trimMores(){
  var t=document.querySelectorAll(".pwarn .txt");
  for(var i=0;i<t.length;i++){
    var b=t[i].parentNode.querySelector(".more");
    if(b)b.style.display=(t[i].scrollHeight>t[i].clientHeight+1)?"":"none";
  }
}
function render(){
  var rows=REVIEW.items.map(function(it){return{it:it,c:classify(it)}});

  var pending=rows.length;
  var clear=rows.filter(function(r){return r.c.state==="clear"}).length;
  var hist=rows.filter(function(r){return r.c.state==="history-open"}).length;
  var flagged=rows.filter(function(r){return r.c.state==="flagged"}).length;
  var total=rows.reduce(function(s,r){return s+r.it.amt},0);
  var ages=rows.map(function(r){return ageDays(r.it.trandate)}).filter(function(a){return a!=null});
  var oldest=ages.length?Math.max.apply(null,ages):0;

  document.getElementById("sub").textContent=pending+" pending your approval";
  freshTick();

  var b="";
  document.getElementById("banners").innerHTML=b;

  fillFilters(rows);
  var vrows=applyView(rows), hidden=rows.length-vrows.length;

  // The Pending tile went with the freshness card: it restated the subtitle directly
  // above it. The rest now count the filtered set against the whole queue.
  var vClear=vrows.filter(function(r){return r.c.state==="clear"}).length;
  var vHist=vrows.filter(function(r){return r.c.state==="history-open"}).length;
  var vFlagged=vrows.filter(function(r){return r.c.state==="flagged"}).length;
  var vTotal=vrows.reduce(function(s,r){return s+r.it.amt},0);
  var vAges=vrows.map(function(r){return ageDays(r.it.trandate)}).filter(function(a){return a!=null});
  var vOldest=vAges.length?Math.max.apply(null,vAges):0;

  // The one line the floating header carries that depends on the filter, so it has to be set
  // before floatPaint(), which is what paints that bar.
  window.__vsum=(hidden>0?vrows.length+" of "+rows.length+" shown":rows.length+" pending")+
                (vFlagged?" · "+vFlagged+" flagged":"")+(vHist?" · "+vHist+" history open":"");

  document.getElementById("cards").innerHTML=
   cd("Clear",ofTotal(vClear,clear),"var(--ok-fg)")+
   cd("History open",ofTotal(vHist,hist),"var(--warn-fg)")+
   cd("Flagged",ofTotal(vFlagged,flagged),"var(--bad-fg)")+
   cd("Oldest",ofTotal(vOldest?vOldest+"d":"–",oldest?oldest+"d":"–"))+
   cd("In queue",ofTotal(total?compactMoney(vTotal):"$0",total?compactMoney(total):"$0"));

  var body="";
  vrows.forEach(function(r){body+=itemRow(r.it,r.c)});
  document.getElementById("rows").innerHTML=
   (hidden>0?'<p class="hid">'+hidden+' item'+(hidden>1?'s':'')+' hidden by the current filter. <a href="#" onclick="resetView();return false">Show everything</a></p>':"")+
   (body||'<div class="empty">'+(viewActive()?"No items match this filter.":"Nothing pending your approval right now.")+'</div>');

  floatPaint();
  trimMores();
}
//__SHARED:dash-of-total__
// Tiles follow the filter, so they can never disagree with the list underneath them.
function ofTotal(v,t){return String(v)===String(t)?String(t)
  :v+'<span class="of"> of '+t+'</span>'}
//__END_SHARED:dash-of-total__
function cd(l,v,col){return '<div class="card"><div class="l">'+l+'</div><div class="v"'+(col?' style="color:'+col+'"':'')+'>'+v+'</div></div>'}

// The PO the bill is APPLIED to, and how that was resolved. Three states, kept distinct on
// purpose: an unlinked or unreadable PO must never render as though it had been confirmed.
// it.poRef comes from the transaction linkage, never from the typed custbody3 reference.
function poLine(it){
  if(!it.poRef&&!it.poLink)return "";
  var st=it.poLink||"", lab, col="";
  if(st==="linked")        lab="Applied to "+esc(it.poRef);
  else if(st==="unlinked"){lab="No PO applied in NetSuite"+(it.poRef?" \u00b7 record names "+esc(it.poRef):"");col="var(--warn-fg)"}
  else if(st==="failed")  {lab="PO linkage could not be read \u00b7 not checked";col="var(--warn-fg)"}
  else                     lab=esc(it.poRef);
  return '<span class="polink"'+(col?' style="color:'+col+'"':'')+'>'+lab+'</span><br>';
}

function itemRow(it,c2){
  // DOM key: the record id, or a negative number the publish step gives a blank-id row, so
  // two such rows never share an element id.
  var k=it.key!=null?it.key:it.id;
  var cls="row";
  var a=ageDays(it.trandate);
  // Verdict rides the card's left rail and a label on the meta line below.
  // Three explicit branches. An unknown state is never drawn as Clear.
  var st=c2.state, vc, vt, vk;
  if(st==="flagged"){vc="var(--bad-fg)";vt="Flagged";vk=" vflag"}
  else if(st==="history-open"){vc="var(--warn-fg)";vt="History open";vk=" vhist"}
  else if(st==="clear"){vc="var(--ok-fg)";vt="Clear";vk=" vclear"}
  else{vc="var(--bad-fg)";vt="Unknown";vk=" vflag"}
  var vlab='<span class="vlab" style="color:'+vc+'">'+vt+'</span> · ';
  var h='<div class="'+cls+vk+'" id="row'+k+'">'+
  '<div class="rh">'+
  '<span class="doc">'+esc(it.type)+' · '+esc(it.doc)+'</span>'+
  '<span class="amt">'+money(it.amt)+'</span></div>'+
  '<p class="ven">'+vlab+esc(it.vendor)+(a!=null?' <span style="color:'+(a>14?"var(--bad-fg)":"var(--ink3)")+'">· '+a+' days pending'+(a>14?' · over 14d':'')+'</span>':'')+'</p>';
  h+='<p class="head">'+esc(it.head)+'</p>'+
  '<ul class="f">'+it.facts.map(function(f){return '<li>'+esc(f)+'</li>'}).join("")+'</ul>'+
  '<div class="po'+(it.poLink==="unlinked"?" unlinked":it.poLink==="failed"?" failed":"")+'">'+poLine(it)+esc(it.po)+
  // A history-open warning is the whole reason for the verdict, so it is never clipped
  // and has no `more` control.
  (it.poWarn?'<div class="pwarn"><span class="lbl">Worth clearing separately</span>'+
   (c2.state==="history-open"
     ?'<span class="full" id="pw'+k+'">'+esc(it.poWarn)+'</span></div>'
     :'<span class="txt" id="pw'+k+'">'+esc(it.poWarn)+'</span>'+
      '<button class="more" onclick="pwtog('+k+',this)">more</button></div>'):'')+'</div>'+
  '<p class="det" id="det'+k+'">'+esc(it.detail)+
   (it.dcut?' <a href="#" onclick="fullDetail('+k+');return false">Full detail ↗</a>':'')+
   (it.att?'<br><span class="att">Read: '+esc(it.att)+'</span>':'')+'</p>'+
  '<div class="acts">'+
  '<span style="flex:1"></span>'+
  '<a href="#" onclick="tog('+k+',this);return false">Show detail</a>'+
  // A blank id has no record to open: no link, never a "?id=" URL that opens nothing.
  (it.id?'<a href="'+recUrl(it.id)+'" target="_blank" rel="noopener" onclick="return nav(this)">Open record</a>':'')+
  '</div>';
  return h+'</div>'
}

function pwtog(id,btn){var t=document.getElementById("pw"+id);if(!t)return;
  var open=t.className.indexOf("open")>=0;
  t.className=open?"txt":"txt open";btn.textContent=open?"more":"less"}
function tog(id,btn){var d=document.getElementById("det"+id);var open=d.style.display==="block";d.style.display=open?"none":"block";btn.textContent=open?"Show detail":"Hide detail"}
// retired: see actionable-retired/netsuite-approval-review/dashboard_template.cut.html, review-only-mode
function fullDetail(k){var it=null;
  for(var i=0;i<REVIEW.items.length;i++){var x=REVIEW.items[i];if((x.key!=null?x.key:x.id)==k){it=x;break}}
  if(it)say("Show me the full detail text for NetSuite "+it.type+" "+it.doc+" (id "+it.id+") exactly as it is written in the review log. Read-only: quote it and change nothing.")}
function sendRun(){say("Run my NetSuite approval check now")}
function say(t){if(window.sendPrompt)window.sendPrompt(t)}

// retired: see actionable-retired/netsuite-approval-review/dashboard_template.cut.html, review-only-mode
//__SHARED:dash-band-track__
// ---- the host's visible band, and the floating header that rides it ---------------------
// This frame does not scroll. It is sized to its own content and the HOST page scrolls, so
// window.innerHeight === document.scrollHeight and window.scrollY never leaves 0. Both
// position:sticky and position:fixed freeze at a document coordinate and slide off screen
// with everything else - which is why the header could not just be made sticky, and why
// nobody has ever seen the floating bar pinned.
//
// IntersectionObserver is the one instrument that reaches across the frame boundary. Its
// intersectionRect is clipped by every ancestor viewport, cross-origin ones included, so from
// in here it is possible to read exactly which slice of this document the reader is looking
// at. rootBounds does come back null - that part really is withheld - but the clipped rect is
// not, and the clipped rect is all this needs.
//
// The instrument has to be a column of CONTIGUOUS TILES rather than one full-height sentinel,
// and that is the whole trick. Thresholds are ratios: a 700px viewport over a 4,000px
// sentinel is 17% of it and stays 17% however far you scroll, so no threshold is ever crossed
// and the callback fires a handful of times for a whole page of scrolling - measured at 4,
// reporting a stale band at three of six offsets. Tiled, the tile straddling the top edge of
// the band is clipped BY that edge, so its intersectionRect.top is the band top exactly, and
// its own visible ratio changes continuously as the reader scrolls, which is what keeps the
// callbacks coming. Measured against both host arrangements: 0.0px error at every offset, and
// a distinct position for all 26 steps of an 8px-step scroll.
var BAND_TILE=100, BAND_MIN=140, bandSeen=new Map(), bandIO=null, bandH=-1;

function bandBuild(){
  var sen=document.getElementById("bandsen");
  if(!sen||!window.IntersectionObserver)return;
  // height:100% of .wrap, so this measures the page
  var h=sen.clientHeight;
  // nothing moved, and re-tiling would only churn
  if(h===bandH)return;
  bandH=h;
  if(bandIO)bandIO.disconnect();
  bandSeen.clear();
  sen.innerHTML="";
  var n=Math.max(1,Math.ceil(h/BAND_TILE));
  for(var k=0;k<n;k++){
    var t=document.createElement("i");
    t.style.height=(k===n-1?Math.max(1,h-k*BAND_TILE):BAND_TILE)+"px";
    sen.appendChild(t);
  }
  // 20 steps per tile puts a threshold every 5px of scroll. Fewer and the bar steps visibly;
  // more buys nothing a reader can see and costs a callback every time one is crossed.
  var th=[]; for(var i=0;i<=20;i++)th.push(i/20);
  bandIO=new IntersectionObserver(bandSaw,{threshold:th});
  for(var j=0;j<sen.children.length;j++)bandIO.observe(sen.children[j]);
}

function bandSaw(es){
  es.forEach(function(e){
    if(e.isIntersecting&&e.intersectionRect.height>0)bandSeen.set(e.target,e.intersectionRect);
    else bandSeen.delete(e.target);
  });
  var top=Infinity,bot=-Infinity;
  bandSeen.forEach(function(r){if(r.top<top)top=r.top; if(r.bottom>bot)bot=r.bottom});
  bandPlace(top===Infinity?null:top,bot);
}

// Show the floating bar only once the real header has left the band, and put it at the top of
// what the reader can actually see. While the real controls are on screen nothing is
// duplicated: a second copy of a control you are already looking at is only clutter.
function bandPlace(top,bot){
  var fh=document.getElementById("floathdr"), tb=document.querySelector(".toolbar"),
      wrap=document.querySelector(".wrap");
  if(!fh||!tb||!wrap)return;
  // BAND_MIN is a design constant, not a measurement: the bar is about 44px, so below this
  // much visible page the bar would be most of what is on screen and would hang out of the
  // sliver it is meant to sit in.
  if(top==null||bot-top<BAND_MIN){fh.style.display="none";return}
  if(tb.getBoundingClientRect().bottom>=top){fh.style.display="none";return}
  // intersectionRect arrives in this document's client coordinates and #floathdr is absolute
  // inside .wrap, so .wrap's own offset has to come off. That offset is read live rather than
  // cached because a host that DID scroll this frame would otherwise place the bar wrongly.
  fh.style.top=Math.round(top-wrap.getBoundingClientRect().top+10)+"px";
  fh.style.display="block";
}

function toFilters(){
  var t=document.querySelector(".toolbar");
  // scrollIntoView from inside a cross-origin frame really does scroll the host's scroller -
  // verified in Chromium, a host at 2500 landing on the frame's own top. It is the only
  // control this page has over where the reader is looking, and it is what makes the floating
  // bar a way BACK to the header rather than a replacement for it.
  if(t)t.scrollIntoView({block:"start"});
}

// What the bar carries. The full header is ~380px of chrome and reproducing that mid-queue
// would cost half a 700px viewport, so what floats is only what is worth having in the second
// before a glance: where you are in the filter, and one press back to the real controls. The
// whole bar is aria-hidden with tabindex="-1" throughout, because it duplicates controls that
// are already in the page and a screen reader gains nothing from meeting them twice.
// It once mirrored the execute button too - retired, see actionable-retired/_shared/
// dash-header-mirror.block, review-only-mode.
function floatPaint(){
  var fh=document.getElementById("floathdr");
  if(!fh)return;
  fh.innerHTML='<div class="floatbar">'+
    '<span class="fc">'+esc(window.__vsum||"")+'</span>'+
    '<span class="fsp"></span>'+
    '<button tabindex="-1" onclick="toFilters()">Filters ↑</button></div>';
}

if(window.ResizeObserver){
  // The page's height changes whenever a filter narrows the queue or a reader opens a detail,
  // and tiles that stopped short of the new bottom would leave the band unreadable down there
  // - no tile intersecting reads as "off screen", so the bar would vanish mid-queue. Observing
  // the wrapper covers every cause at once, the first layout included, so no render path has
  // to remember to call bandBuild(). The sentinel column is absolutely positioned and
  // contributes no height, so re-tiling cannot feed itself.
  new ResizeObserver(function(){bandBuild()}).observe(document.querySelector(".wrap"));
} else { bandBuild(); }
//__END_SHARED:dash-band-track__
//__SHARED:dash-render-tail__
// retired: see actionable-retired/_shared/dash-render-tail.cut.block, review-only-mode
render();
// The tick ages the freshness line and flips the Snapshot pill. It must NEVER call
// render(), which rebuilds #rows from scratch: that silently collapsed every expanded
// detail and every opened warning, and which rows survived depended only on where the
// 60s boundary fell relative to the clicks - so it read as random. Measured on v9.
// The data is a snapshot and never changes, so there is nothing else for a tick to do.
setInterval(freshTick, 60000);
// Last line of the file. The inline guard reads window.__dashOK to learn that this file ran to the
// end and that the stylesheet is applied (--dash-css is declared on :root in dashboard.css). A
// dynamically added script does not wait for a stylesheet, so a failed first probe tries once
// more when the stylesheet's own load event fires.
function dashProbe(){window.__dashOK=!!getComputedStyle(document.documentElement).getPropertyValue("--dash-css").trim();return window.__dashOK}
if(!dashProbe()){var dashLink=document.querySelector("link[data-dash]");if(dashLink)dashLink.addEventListener("load",dashProbe)}
//__END_SHARED:dash-render-tail__
