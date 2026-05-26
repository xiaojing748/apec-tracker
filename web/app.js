(function(){"use strict";
var DATA_URL="../data/articles.json",allArticles=[],activeView="list";
var AF={cat:new Set(["数据跨境与隐私保护","AI治理","电信与网络治理","数字经济","互联互通","供应链安全","地缘政治","2026中国年","其他APEC动态"]),st:new Set(["官方公报","权威媒体"]),dt:new Set(),ab:new Set(),gf:new Set(),pt:new Set(),tr:"7",mo:"",sq:"",sr:"date"};

var CATS=["数据跨境与隐私保护","AI治理","电信与网络治理","数字经济","互联互通","供应链安全","地缘政治","2026中国年","其他APEC动态"];
var STS=["官方公报","权威媒体"];
var DTS={official_statement:"官方声明",press_release:"新闻稿",meeting_minutes:"会议纪要",policy_document:"政策文件",report:"研究报告",speech:"演讲致辞",regulation:"法规标准",media_report:"媒体报道",academic:"学术论文"};
var ABS={TELWG:"TELWG 电信工作组",DESG:"DESG 数字经济转向组",ECSG:"ECSG 电商转向组",DPS:"DPS 数据隐私小组",SOM:"SOM 高官会",MRT:"MRT 贸易部长",ABAC:"ABAC 工商理事会",CTI:"CTI 贸易委员会",TELMIN:"TELMIN 数字经济部长"};
var GFS={china:"中国",usa:"美国",japan:"日本",korea:"韩国",asean:"东盟",australia:"澳大利亚",russia:"俄罗斯",canada:"加拿大",latin_america:"拉丁美洲",global:"全球/多边",regional:"区域"};
var PTS={CBPR:"CBPR",AIDER:"AIDER",DFFT:"DFFT",FTAAP:"FTAAP",DEPA:"DEPA",RCEP:"RCEP",CPTPP:"CPTPP",Connectivity_Blueprint:"互联互通蓝图",Digital_Trade:"数字贸易",AI_Governance:"AI治理",Cybersecurity:"网络安全",Privacy_Framework:"隐私框架"};

function gel(id){return document.getElementById(id)}
function eh(s){if(!s)return"";return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;")}
function ce(s){if(!s)return"";return'"'+s.replace(/"/g,'""')+'"'}
function pad(n){return n<10?"0"+n:""+n}
function gcc(c){var m={};CATS.forEach(function(v,i){m[v]=["cbpr","ai","telecom","digital","digital","geo","geo","china","other"][i]||"other"});return m[c]||"other"}

function db(fn,ms){var t;return function(){var c=this,a=arguments;clearTimeout(t);t=setTimeout(function(){fn.apply(c,a)},ms)}}

function toast(m){var t=gel("toast");t.textContent=m;t.classList.add("show");clearTimeout(t._t);t._t=setTimeout(function(){t.classList.remove("show")},2000)}

function dlFile(fn,ct,mt){var b=new Blob([ct],{type:mt+";charset=utf-8"});var u=URL.createObjectURL(b);var a=document.createElement("a");a.href=u;a.download=fn;document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(u)}

function init(){if(window.__APEC_DATA__){loadData(window.__APEC_DATA__);return}
var x=new XMLHttpRequest();x.open("GET",DATA_URL,true);
x.onload=function(){if(x.status===200){try{loadData(JSON.parse(x.responseText))}catch(e){se("JSON error")}}else se("HTTP "+x.status)};
x.onerror=function(){se("Network error")};x.send()}

function se(m){gel("updateTime").textContent=m;gel("contentArea").innerHTML='<div class="no-results"><div class="icon">&#x26A0;</div><p>'+eh(m)+'</p></div>'}

function loadData(d){
allArticles=d.articles||[];
allArticles.forEach(function(a){
if(!a.doc_type)a.doc_type=["media_report"];if(!a.apec_bodies)a.apec_bodies=[];
if(!a.geo_focus)a.geo_focus=["regional"];if(!a.policy_tags)a.policy_tags=[];
if(!a.relevance)a.relevance=50;if(!a.notes)a.notes="";if(a.starred===undefined)a.starred=false});
gel("updateTime").textContent="最后更新："+(d.last_updated||"未知");
gel("statTotal").textContent=d.total_articles||allArticles.length;
gel("statMonth").textContent=d.monthly_count||0;
gel("statToday").textContent=d.today_count||0;
popMonths();buildFilters();bindEvents();applyAll();updateQP()}

function popMonths(){var m={};allArticles.forEach(function(a){var k=(a.date||"").substring(0,7);if(k)m[k]=(m[k]||0)+1});
var s=Object.keys(m).sort().reverse();var sel=gel("monthFilter");while(sel.options.length>1)sel.remove(1);
s.forEach(function(k){var o=document.createElement("option");o.value=k;o.textContent=k+" ("+m[k]+"篇)";sel.appendChild(o)})}

function buildFilters(){
buildCG("categoryFilters",CATS.reduce(function(o,v){o[v]=v;return o},{},),null,AF.cat,"category");
buildCG("sourceTypeFilters",STS.reduce(function(o,v){o[v]=v;return o},{},),null,AF.st,"sourceType");
buildCG("docTypeFilters",DTS,DTS,AF.dt,"docType");
buildCG("apecBodyFilters",ABS,ABS,AF.ab,"apecBody");
buildCG("geoFocusFilters",GFS,GFS,AF.gf,"geoFocus");
buildCG("policyTagFilters",PTS,PTS,AF.pt,"policyTag")}

function buildCG(cid,items,labels,fs,fk){
var c=gel(cid);if(!c)return;var h="";
for(var k in items){if(!items.hasOwnProperty(k))continue;
var v=items[k],lb=labels?labels[k]||v:v,ch=fs.has(v)?" checked":"";
h+='<label><input type="checkbox" data-filter="'+fk+'" value="'+eh(v)+'"'+ch+'> '+eh(lb)+'</label>'}
c.innerHTML=h}

function scf(type,fs){fs.clear();var boxes=document.querySelectorAll('[data-filter="'+type+'"]:checked');
for(var i=0;i<boxes.length;i++)fs.add(boxes[i].value)}

function bindEvents(){
gel("btnApply").onclick=applyAll;gel("resetFilters").onclick=resetAll;
gel("timeFilter").onchange=function(){AF.tr=this.value};
gel("monthFilter").onchange=function(){AF.mo=this.value};
gel("searchBox").oninput=db(function(){AF.sq=this.value.trim().toLowerCase();applyAll()},300);
gel("sortSelect").onchange=function(){AF.sr=this.value;applyAll()};
var tabs=document.querySelectorAll(".view-tab");
for(var i=0;i<tabs.length;i++)tabs[i].onclick=function(){
activeView=this.dataset.view;
document.querySelectorAll(".view-tab").forEach(function(t){t.classList.remove("active")});
this.classList.add("active");
gel("dashboardArea").style.display=activeView==="dashboard"?"block":"none";
gel("contentArea").style.display=activeView==="dashboard"?"none":"block";
if(activeView==="dashboard")updateDB();else renderArts()};
gel("btnToggleAdd").onclick=function(){var f=gel("addFormSection");f.style.display=f.style.display==="none"?"block":"none"};
gel("btnAddArticle").onclick=addManual;gel("detailModal").onclick=function(e){if(e.target===this)closeModal()};
gel("btnFeedback").onclick=subFB;gel("btnExportMD").onclick=expMD;gel("btnExportCSV").onclick=expCSV;
gel("quarterSelect").onchange=updateQP;
var today=new Date().toISOString().substring(0,10);var di=gel("addDate");if(di)di.value=today}

function applyAll(){scf("category",AF.cat);scf("sourceType",AF.st);scf("docType",AF.dt);
scf("apecBody",AF.ab);scf("geoFocus",AF.gf);scf("policyTag",AF.pt);
AF.tr=gel("timeFilter").value;AF.mo=gel("monthFilter").value;
if(activeView==="dashboard")updateDB();else renderArts();updateQP()}

function resetAll(){
AF.cat=new Set(CATS);AF.st=new Set(STS);AF.dt=new Set();AF.ab=new Set();AF.gf=new Set();AF.pt=new Set();
AF.tr="7";AF.mo="";AF.sq="";AF.sr="date";
gel("timeFilter").value="7";gel("monthFilter").value="";gel("searchBox").value="";gel("sortSelect").value="date";
buildFilters();applyAll()}

function filterArts(){
var f=allArticles.slice();var now=new Date();
if(AF.tr!=="all"){var days=parseInt(AF.tr);var cutoff=new Date(now.getTime()-days*86400000).toISOString().substring(0,10);f=f.filter(function(a){return a.date>=cutoff})}
if(AF.mo)f=f.filter(function(a){return(a.date||"").substring(0,7)===AF.mo});
if(AF.cat.size<CATS.length)f=f.filter(function(a){return(a.categories||[]).some(function(c){return AF.cat.has(c)})});
if(AF.st.size<STS.length)f=f.filter(function(a){return AF.st.has(a.source_type)});
if(AF.dt.size>0)f=f.filter(function(a){return(a.doc_type||[]).some(function(d){return AF.dt.has(d)})});
if(AF.ab.size>0)f=f.filter(function(a){return(a.apec_bodies||[]).some(function(b){return AF.ab.has(b)})});
if(AF.gf.size>0)f=f.filter(function(a){return(a.geo_focus||[]).some(function(g){return AF.gf.has(g)})});
if(AF.pt.size>0)f=f.filter(function(a){return(a.policy_tags||[]).some(function(p){return AF.pt.has(p)})});
if(AF.sq){var q=AF.sq;f=f.filter(function(a){var t=((a.title||"")+" "+(a.source||"")+" "+(a.summary||"")+" "+(a.notes||"")).toLowerCase();return t.indexOf(q)!==-1})}
if(AF.sr==="relevance")f.sort(function(a,b){return(b.relevance||0)-(a.relevance||0)});
else if(AF.sr==="title")f.sort(function(a,b){return(a.title||"").localeCompare(b.title||"","zh")});
else f.sort(function(a,b){return(b.date||"").localeCompare(a.date||"")});
return f}

function rAF(){
var chips=[];
if(AF.tr!=="all"){var rl={"1":"今天","3":"最近3天","7":"最近一周","30":"最近一月","90":"本季度"};chips.push({label:rl[AF.tr]||AF.tr,key:"tr"})}
if(AF.mo)chips.push({label:AF.mo,key:"mo"});
if(AF.sq)chips.push({label:"搜索: "+AF.sq,key:"sq"});
var h=chips.map(function(c){return '<span class="filter-chip">'+eh(c.label)+' <span class="chip-x" data-clear="'+c.key+'">&times;</span></span>'}).join("");
gel("activeFilters").innerHTML=h;
var xbtns=document.querySelectorAll(".chip-x");for(var i=0;i<xbtns.length;i++)xbtns[i].onclick=function(){
var k=this.dataset.clear;
if(k==="tr"){gel("timeFilter").value="all";AF.tr="all"}
if(k==="mo"){gel("monthFilter").value="";AF.mo=""}
if(k==="sq"){gel("searchBox").value="";AF.sq=""}
applyAll()}}

function renderArts(){
var f=filterArts();gel("resultCount").textContent=f.length+" 条结果";rAF();var area=gel("contentArea");
if(f.length===0){area.innerHTML='<div class="no-results"><div class="icon">&#x1F50D;</div><p>没有匹配的结果</p><p style="font-size:0.8rem;color:var(--text-muted)">尝试调整筛选条件或搜索关键词</p></div>';return}
if(activeView==="timeline")area.innerHTML=rTL(f);
else if(activeView==="grid")area.innerHTML='<div class="article-grid">'+f.map(rCard).join("")+'</div>';
else area.innerHTML='<div class="article-list">'+f.map(rCard).join("")+'</div>';
bindCards()}

function rCard(a){
var sc=a.starred?" starred":"";
var ct=(a.categories||[]).map(function(c){return '<span class="tag tag-'+gcc(c)+'">'+eh(c)+'</span>'}).join("");
var dtl="";if(a.doc_type&&a.doc_type.length>0){var dt=a.doc_type[0];dtl='<span class="tag tag-doc">'+eh(DTS[dt]||dt)+'</span>'}
var bt=(a.apec_bodies||[]).slice(0,2).map(function(b){return '<span class="tag tag-body">'+eh(b)+'</span>'}).join("");
var pb=(a.policy_tags||[]).slice(0,2).map(function(p){return '<span class="tag tag-policy">'+eh(p)+'</span>'}).join("");
var rel=a.relevance||50;var rc=rel>=80?"var(--accent-red)":rel>=60?"var(--accent-gold)":"var(--text-muted)";
var idx=allArticles.indexOf(a);
return '<div class="article-card" data-idx="'+idx+'"><div class="card-top"><div style="flex:1;min-width:0"><div class="card-title">'+eh(a.title||"无标题")+'</div><div class="card-meta"><span class="card-source">'+eh(a.source||"未知")+'</span><span class="card-date">'+(a.date||"")+'</span><span class="card-relevance" style="color:'+rc+'">相关度 '+rel+'</span></div><div class="card-tags">'+ct+dtl+bt+pb+'</div></div><button class="star-btn'+sc+'" data-action="star">&starf;</button></div></div>'}

function rTL(arts){
var g={};arts.forEach(function(a){var d=a.date||"未知";if(!g[d])g[d]=[];g[d].push(a)});
var ds=Object.keys(g).sort().reverse();var h='<div class="timeline-container">';
ds.forEach(function(d){h+='<div class="timeline-date">'+eh(d)+'</div>';g[d].forEach(function(a){h+='<div class="timeline-item">'+rCard(a)+'</div>'})});
h+='</div>';return h}

function bindCards(){
var cards=document.querySelectorAll(".article-card");
for(var i=0;i<cards.length;i++)cards[i].onclick=function(e){
if(e.target.closest(".star-btn")){e.stopPropagation();var idx=parseInt(this.dataset.idx);allArticles[idx].starred=!allArticles[idx].starred;toast(allArticles[idx].starred?"已收藏":"已取消收藏");renderArts();return}
openDetail(parseInt(this.dataset.idx))}}

function openDetail(idx){
var a=allArticles[idx];var c=gel("detailContent");
var ct=(a.categories||[]).map(function(c){return '<span class="tag tag-'+gcc(c)+'">'+eh(c)+'</span>'}).join("");
var bt=(a.apec_bodies||[]).map(function(b){return '<span class="tag tag-body">'+eh(b)+'</span>'}).join("")||"无";
var gt=(a.geo_focus||[]).map(function(g){return '<span class="tag tag-geo-tag">'+eh(GFS[g]||g)+'</span>'}).join("")||"区域";
var pt=(a.policy_tags||[]).map(function(p){return '<span class="tag tag-policy">'+eh(p)+'</span>'}).join("")||"无";
var dts=(a.doc_type||[]).map(function(d){return DTS[d]||d}).join(", ")||"媒体报道";
var notes=a.notes||"";
c.innerHTML='<button class="modal-close" onclick="document.getElementById(&quot;detailModal&quot;).classList.remove(&quot;active&quot;)">&times;</button>'
+'<div class="detail-title">'+eh(a.title||"无标题")+'</div>'
+'<a class="detail-url" href="'+eh(a.url)+'" target="_blank" rel="noopener">'+eh(a.url)+' &#x2197;</a>'
+'<div class="detail-meta-grid">'
+'<div><span class="meta-label">来源</span><br>'+eh(a.source||"未知")+'</div>'
+'<div><span class="meta-label">来源类型</span><br>'+eh(a.source_type||"")+'</div>'
+'<div><span class="meta-label">日期</span><br>'+(a.date||"未知")+'</div>'
+'<div><span class="meta-label">相关度</span><br>'+(a.relevance||50)+'</div>'
+'<div><span class="meta-label">文档类型</span><br>'+dts+'</div>'
+'<div><span class="meta-label">议题</span><br>'+ct+'</div>'
+'<div><span class="meta-label">APEC机构</span><br>'+bt+'</div>'
+'<div><span class="meta-label">地理焦点</span><br>'+gt+'</div>'
+'<div><span class="meta-label">政策标签</span><br>'+pt+'</div>'
+'</div>'
+'<div style="margin-bottom:4px"><span class="meta-label">分析笔记</span></div>'
+'<textarea class="detail-notes-area" id="detailNotes" placeholder="添加你的分析备注...">'+eh(notes)+'</textarea>'
+'<div style="display:flex;gap:8px">'
+'<button class="btn primary" id="btnSaveNotes">保存笔记</button>'
+'<button class="btn" onclick="window.open(&quot;'+eh(a.url)+'&quot;,&quot;_blank&quot;)">打开原文</button>'
+'<span style="margin-left:auto;line-height:36px;font-size:0.78rem;color:var(--text-muted)" id="notesStatus"></span>'
+'</div>';
gel("btnSaveNotes").onclick=function(){allArticles[idx].notes=gel("detailNotes").value;gel("notesStatus").textContent="已保存";toast("笔记已保存")};
gel("detailModal").classList.add("active")}
function closeModal(){gel("detailModal").classList.remove("active")}

function addManual(){
var t=gel("addTitle").value.trim(),u=gel("addUrl").value.trim(),d=gel("addDate").value,st=gel("addSourceType").value,s=gel("addSource").value.trim()||"手动添加",sm=gel("addSummary").value.trim(),ca=gel("addCategory").value;
if(!t||!u){toast("标题和链接不能为空");return}
var art={title:t,url:u,date:d||new Date().toISOString().substring(0,10),source:s,source_type:st,summary:sm,categories:ca?[ca]:[],doc_type:["media_report"],apec_bodies:[],geo_focus:["regional"],policy_tags:[],relevance:60,notes:"",starred:false,_manual:true};
if(!ca)art.categories=ac(t,sm);
allArticles.unshift(art);gel("addTitle").value="";gel("addUrl").value="";gel("addSummary").value="";gel("addSource").value="";gel("addCategory").value="";
popMonths();applyAll();toast("文章已添加")}
function ac(t,sm){var tx=(t+" "+sm).toLowerCase();var cs=[];var rs={"数据跨境与隐私保护":["数据跨境","跨境数据","数据隐私","cbpr","privacy","个人信息"],"AI治理":["ai","人工智能","智能","算法"],"电信与网络治理":["电信","telwg","网络安全","5g"],"数字经济":["数字","电商","e-commerce","fintech"],"互联互通":["互联互通","connectivity","基础设施"],"供应链安全":["供应链","supply chain"],"地缘政治":["贸易","trade","关税","tariff","多边"]};
for(var k in rs){if(rs.hasOwnProperty(k)){for(var i=0;i<rs[k].length;i++){if(tx.indexOf(rs[k][i])!==-1){cs.push(k);break}}}}
if(cs.length===0)cs.push("其他APEC动态");return cs}

function updateDB(){
var f=filterArts();gel("resultCount").textContent=f.length+" 条结果";
var tc={};CATS.forEach(function(c){tc[c]=0});f.forEach(function(a){(a.categories||[]).forEach(function(c){if(tc[c]!==undefined)tc[c]++})});
var mx=Math.max.apply(null,Object.values(tc))||1;
var tcl={cbpr:"cbpr",ai:"ai",telecom:"telecom",digital:"digital",geo:"geo",china:"china",other:"other"};
var th="";for(var k in tc){if(tc.hasOwnProperty(k)&&tc[k]>0){var pct=Math.round(tc[k]/mx*100);var cls=tcl[gcc(k)]||"digital";th+='<div class="chart-bar"><span class="bar-label">'+eh(k)+'</span><span class="bar-track"><span class="bar-fill '+cls+'" style="width:'+pct+'%"></span></span><span class="bar-count">'+tc[k]+'</span></div>'}}
gel("topicChart").innerHTML=th||'<p style="color:var(--text-muted);font-size:0.8rem">暂无数据</p>';

var sc={};f.forEach(function(a){var s=a.source||"未知";sc[s]=(sc[s]||0)+1});
var ss=Object.entries(sc).sort(function(a,b){return b[1]-a[1]}).slice(0,8);var ms=ss.length>0?ss[0][1]:1;
var sh="";ss.forEach(function(p){var pct=Math.round(p[1]/ms*100);sh+='<div class="chart-bar"><span class="bar-label">'+eh(p[0].substring(0,10))+'</span><span class="bar-track"><span class="bar-fill telecom" style="width:'+pct+'%"></span></span><span class="bar-count">'+p[1]+'</span></div>'});
gel("sourceChart").innerHTML=sh||'<p style="color:var(--text-muted);font-size:0.8rem">暂无数据</p>';

var dc={};f.forEach(function(a){(a.doc_type||[]).forEach(function(d){dc[d]=(dc[d]||0)+1})});
var ds=Object.entries(dc).sort(function(a,b){return b[1]-a[1]});var md=ds.length>0?ds[0][1]:1;
var dh="";ds.forEach(function(p){var lb=DTS[p[0]]||p[0];var pct=Math.round(p[1]/md*100);dh+='<div class="chart-bar"><span class="bar-label">'+eh(lb)+'</span><span class="bar-track"><span class="bar-fill cbpr" style="width:'+pct+'%"></span></span><span class="bar-count">'+p[1]+'</span></div>'});
gel("docTypeChart").innerHTML=dh||'<p style="color:var(--text-muted);font-size:0.8rem">暂无数据</p>';

var mc={};f.forEach(function(a){var m=(a.date||"").substring(0,7);if(m)mc[m]=(mc[m]||0)+1});
var ms2=Object.entries(mc).sort();var mh="";ms2.forEach(function(p){var pct=Math.min(100,p[1]*5);mh+='<div class="chart-bar"><span class="bar-label">'+p[0]+'</span><span class="bar-track"><span class="bar-fill ai" style="width:'+pct+'%"></span></span><span class="bar-count">'+p[1]+'</span></div>'});
gel("monthlyChart").innerHTML=mh||'<p style="color:var(--text-muted);font-size:0.8rem">暂无数据</p>'}

function gQA(){
var q=gel("quarterSelect").value;var parts=q.split("-");var yr=parts[0],qn=parseInt(parts[1].substring(1));
var sm=(qn-1)*3+1,em=qn*3;var sd=yr+"-"+pad(sm)+"-01";
var ed=new Date(parseInt(yr),em,0).getDate();var ed2=yr+"-"+pad(em)+"-"+pad(ed);
return allArticles.filter(function(a){return a.date>=sd&&a.date<=ed2}).sort(function(a,b){return(a.date||"").localeCompare(b.date||"")})}

function updateQP(){var arts=gQA();gel("quarterCount").textContent=arts.length+" 篇";
var pv=gel("quarterPreview");pv.innerHTML=arts.slice(0,10).map(function(a){return '<div style="padding:4px 0;border-bottom:1px solid var(--border)"><span style="color:var(--text-muted);font-family:var(--font-mono);font-size:0.7rem">'+(a.date||"")+'</span> '+eh(a.title)+'</div>'}).join("")+(arts.length>10?'<p style="color:var(--text-muted);margin-top:8px">...共 '+arts.length+' 篇</p>':"")}

function expMD(){
var arts=gQA();var q=gel("quarterSelect").value;var md="# APEC 追踪季度报告 — "+q+"\n\n> 自动生成于 "+new Date().toISOString().substring(0,10)+" | 共 "+arts.length+" 篇\n\n---\n\n";
var gr={};arts.forEach(function(a){(a.categories||["未分类"]).forEach(function(c){if(!gr[c])gr[c]=[];gr[c].push(a)})});
for(var k in gr){if(gr.hasOwnProperty(k)){md+="## "+k+" ("+gr[k].length+"篇)\n\n";gr[k].forEach(function(a){md+="- **"+(a.title||"无标题")+"**\n  - 来源: "+(a.source||"未知")+" | 日期: "+(a.date||"")+"\n  - 链接: "+(a.url||"")+"\n"+(a.notes?"  - 笔记: "+a.notes+"\n":"")+"\n"})}}
dlFile("APEC-"+q+"-report.md",md,"text/markdown");toast("Markdown 报告已下载")}

function expCSV(){
var arts=gQA();var q=gel("quarterSelect").value;var csv="标题,来源,日期,来源类型,议题,文档类型,相关度,链接,笔记\n";
arts.forEach(function(a){csv+=ce(a.title)+","+ce(a.source)+","+(a.date||"")+","+ce(a.source_type)+","+ce((a.categories||[]).join("; "))+","+ce((a.doc_type||[]).join("; "))+","+(a.relevance||0)+","+ce(a.url)+","+ce(a.notes||"")+"\n"});
dlFile("APEC-"+q+"-data.csv","\uFEFF"+csv,"text/csv");toast("CSV 数据已下载")}

function subFB(){
var tx=gel("feedbackText").value.trim();if(!tx){toast("请输入反馈内容");return}
var ft=document.querySelector('input[name="fbType"]:checked').value;
var ti="["+ft+"] 用户反馈 - "+new Date().toISOString().substring(0,10);
var bd="反馈类型: "+ft+"\n\n"+tx+"\n\n---\n自动提交于 "+new Date().toISOString();
var iu="https://github.com/xiaojing748/apec-tracker/issues/new?title="+encodeURIComponent(ti)+"&body="+encodeURIComponent(bd)+"&labels=feedback";
window.open(iu,"_blank");gel("feedbackText").value="";toast("已跳转到 GitHub Issue，请提交")}

init();
})();
