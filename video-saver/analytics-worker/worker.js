/**
 * Deploy separately with a D1 binding named MARKETING_DB.
 * All events are anonymous DAILY COUNTS. No raw IP, UA, referrer or URL stored.
 * Set VIDKIVA_ANALYTICS_ENDPOINT in the site's marketing.js only after deployment.
 * Protect the route with Cloudflare rate limiting / bot rules for production.
 */
const EVENTS=new Set(["landing_view","demo_play","presskit_download","store_click_ios","store_click_android"]);
const SOURCES=new Set(["reddit","youtube","tiktok","xiaohongshu","xhs","google","bing","newsletter","website","direct","press","other"]);
const MEDIUMS=new Set(["community","organic_social","social","video","search","email","referral","paid_social","other"]);
const SAFE=/^[a-z0-9_-]{1,64}$/;
function cors(origin){const allowed=origin==="https://yuege.online"||origin==="https://www.yuege.online";return {"Access-Control-Allow-Origin":allowed?origin:"https://yuege.online","Access-Control-Allow-Methods":"POST, OPTIONS","Access-Control-Allow-Headers":"Content-Type","Cache-Control":"no-store","Vary":"Origin"}}
function normalize(v,fallback){if(typeof v!=="string")return fallback;v=v.toLowerCase();return SAFE.test(v)?v:fallback}
export default {async fetch(request,env){
 const origin=request.headers.get("Origin");
 const headers=cors(origin);
 if(request.method==="OPTIONS"){return origin==="https://yuege.online"||origin==="https://www.yuege.online"?new Response(null,{status:204,headers}):new Response("Forbidden",{status:403,headers})}
 if(request.method!=="POST")return new Response("Method Not Allowed",{status:405,headers});
 if(origin!=="https://yuege.online"&&origin!=="https://www.yuege.online")return new Response("Forbidden",{status:403,headers});
 if(!request.headers.get("Content-Type")?.startsWith("application/json"))return new Response("Unsupported Media Type",{status:415,headers});
 if(Number(request.headers.get("Content-Length")||0)>2048)return new Response("Too Large",{status:413,headers});
 let payload;try{payload=await request.json()}catch{return new Response("Bad Request",{status:400,headers})}
 const event=normalize(payload?.event,"");if(!EVENTS.has(event))return new Response("Bad Event",{status:400,headers});
 const source=normalize(payload?.source,"direct");const medium=normalize(payload?.medium,"other");
 const campaign=normalize(payload?.campaign,"none");const content=normalize(payload?.content,"none");
 const locale=payload?.locale==="zh-CN"?"zh-CN":"en";
 const day=new Date().toISOString().slice(0,10);
 if(!env.MARKETING_DB)return new Response("Not Configured",{status:503,headers});
 try{
 await env.MARKETING_DB.prepare(`INSERT INTO marketing_daily(day,event,source,medium,campaign,content,locale,total)
 VALUES(?,?,?,?,?,?,?,1)
 ON CONFLICT(day,event,source,medium,campaign,content,locale)
 DO UPDATE SET total=marketing_daily.total+1`).bind(day,event,SOURCES.has(source)?source:"other",MEDIUMS.has(medium)?medium:"other",campaign,content,locale).run();
 return new Response(null,{status:204,headers});
 }catch{return new Response("Internal Error",{status:500,headers})}
}};