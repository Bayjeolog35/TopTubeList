// netlify/functions/download-subtitles.js
const { YoutubeTranscript } = require('youtube-transcript');

function getYouTubeId(url) {
  try {
    const u = new URL(url);
    if (u.hostname.includes('youtu.be')) return u.pathname.slice(1);
    if (u.searchParams.get('v')) return u.searchParams.get('v');
    const m = u.pathname.match(/\/(embed|shorts)\/([^/?]+)/);
    return m ? m[2] : null;
  } catch { return null; }
}

function toTxt(ts){ return ts.map(t=>t.text).join('\n').trim()+'\n'; }
function toSrt(ts){
  const toTime=ms=>{const s=Math.floor(ms/1000),msR=ms%1000;
    const hh=String(Math.floor(s/3600)).padStart(2,'0');
    const mm=String(Math.floor((s%3600)/60)).padStart(2,'0');
    const ss=String(s%60).padStart(2,'0');
    const mmm=String(msR).padStart(3,'0');
    return `${hh}:${mm}:${ss},${mmm}`;};
  return ts.map((t,i,a)=>{const start=Math.round(t.offset);
    const next=a[i+1]?.offset; const dur=t.duration||(next?next-t.offset:2000);
    const end=Math.round(t.offset+dur);
    return `${i+1}\n${toTime(start)} --> ${toTime(end)}\n${t.text}\n`;})
    .join('\n').trim()+'\n';
}
function toVtt(ts){
  const toTime=ms=>{const s=Math.floor(ms/1000),msR=ms%1000;
    const hh=String(Math.floor(s/3600)).padStart(2,'0');
    const mm=String(Math.floor((s%3600)/60)).padStart(2,'0');
    const ss=String(s%60).padStart(2,'0');
    const mmm=String(msR).padStart(3,'0');
    return `${hh}:${mm}:${ss}.${mmm}`;};
  const body=ts.map((t,i,a)=>{const start=Math.round(t.offset);
    const next=a[i+1]?.offset; const dur=t.duration||(next?next-t.offset:2000);
    const end=Math.round(t.offset+dur);
    return `${toTime(start)} --> ${toTime(end)}\n${t.text}\n`;}).join('\n');
  return `WEBVTT\n\n${body}`.trim()+'\n';
}

exports.handler = async (event) => {
  try {
    const qs = event.queryStringParameters || {};
    const url = qs.video_url || qs.url || '';
    const format = (qs.format || 'txt').toLowerCase();
    const vid = getYouTubeId(url);

    if (!vid) {
      return { statusCode: 400, headers:{'Content-Type':'text/plain; charset=utf-8','Access-Control-Allow-Origin':'*'}, body: 'Invalid or missing YouTube URL.' };
    }

    let transcript = null;
    try { transcript = await YoutubeTranscript.fetchTranscript(vid, { lang: 'en' }); } catch {}
    if (!transcript?.length) { try { transcript = await YoutubeTranscript.fetchTranscript(vid, { lang: 'en-US' }); } catch {} }
    if (!transcript?.length) { try { transcript = await YoutubeTranscript.fetchTranscript(vid); } catch {} }

    if (!transcript?.length) {
      return { statusCode: 404, headers:{'Content-Type':'text/plain; charset=utf-8','Access-Control-Allow-Origin':'*'}, body: 'No subtitles found for this video.' };
    }

    let payload, mime, ext;
    if (format === 'srt') { payload = toSrt(transcript); mime='text/plain; charset=utf-8'; ext='srt'; }
    else if (format === 'vtt') { payload = toVtt(transcript); mime='text/vtt; charset=utf-8'; ext='vtt'; }
    else { payload = toTxt(transcript); mime='text/plain; charset=utf-8'; ext='txt'; }

    return {
  statusCode: 200,
  headers: {
    "Content-Type": "text/plain; charset=utf-8",
    "Content-Disposition": "attachment; filename=\"subtitles.srt\""
  },
  body: srtData
};

  } catch (err) {
    return { statusCode: 500, headers:{'Content-Type':'text/plain; charset=utf-8','Access-Control-Allow-Origin':'*'}, body: `Subtitle service error: ${err?.message || 'Internal error'}` };
  }
};
