// Run with: node --test video-saver/tests/marketing.test.mjs
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";
import test from "node:test";
const here=path.dirname(fileURLToPath(import.meta.url));
const script=fs.readFileSync(path.join(here,"../assets/marketing.js"),"utf8");
function render(url,token=""){
 const loc=new URL(url), session=new Map();
 const store={href:"",rel:"",addEventListener(){}};
 const press={href:"",getAttribute(){return "/video-saver/press/";},addEventListener(){}};
 const document={documentElement:{lang:"en"},querySelectorAll(s){if(s==="[data-ios-download]")return [store];if(s==="[data-attribution-link]")return [press];return []}};
 const storage={getItem:k=>session.get(k)||null,setItem:(k,v)=>session.set(k,v)};
 const code=script.replace('appleProviderToken:""', 'appleProviderToken:"'+token+'"');
 vm.runInNewContext(code,{URL,URLSearchParams,location:loc,document,sessionStorage:storage,fetch:()=>Promise.resolve(),console});
 return {store:store.href,press:press.href,session:session.get("vidkiva_first_touch")};
}
test("unconfigured pt never adds invalid App Store campaign parameters",()=>{
 const x=render("https://yuege.online/video-saver/?utm_source=reddit&utm_medium=community&utm_campaign=launch_202611&utm_content=watchlater");
 const url=new URL(x.store);
 assert.equal(url.origin,"https://apps.apple.com");
 assert.equal(url.pathname,"/app/id6829142265");
 assert.equal(url.searchParams.has("pt"),false);
 assert.match(x.press,/utm_source=reddit/);
});
test("real numeric provider token adds a stable source-specific campaign",()=>{
 const x=render("https://yuege.online/video-saver/?utm_source=youtube&utm_medium=video&utm_campaign=launch_202611&utm_content=demo1","1234567");
 const url=new URL(x.store);
 assert.equal(url.searchParams.get("pt"),"1234567");
 assert.equal(url.searchParams.get("ct"),"launch_202611_youtube_demo1");
 assert.equal(url.searchParams.get("mt"),"8");
});
test("untrusted source is not retained or used as a redirect",()=>{
 const x=render("https://yuege.online/video-saver/?utm_source=https://evil.test&utm_campaign=launch_%3Cscript%3E","badtoken");
 assert.equal(new URL(x.store).origin,"https://apps.apple.com");
 assert.equal(new URL(x.store).searchParams.has("pt"),false);
 assert.doesNotMatch(x.press,/evil/);
});
