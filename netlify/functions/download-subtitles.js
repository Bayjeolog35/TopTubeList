// netlify/functions/download-subtitles.js
const { YoutubeTranscript } = require('youtube-transcript');

// URL'den video id'sini çek
function getYouTubeId(url) {
  try {
    const u = new URL(url);
    if (u.hostname.includes('youtu.be')) return u.pathname.slice(1);
    if (u.searchParams.get('v')) return u.searchParams.get('v');
    const m = u.pathname.match(/\/(embed|shorts)\/([^/?]+)/);
    return m ? m[2] : null;
  } catch {
    return null;
  }
}

// TXT dönüştürücü
function toTxt(transcript) {
  return transcript.map(t => t.text).join('\n').trim() + '\n';
}

// SRT dönüştürücü
function toSrt(transcript) {
  const toTime = ms => {
    const s = Math.floor(ms / 1000), msR = ms % 1000;
    const hh = String(Math.floor(s / 3600)).padStart(2,'0');
    const mm = String(Math.floor((s % 3600) / 60)).padStart(2,'0');
    const ss = String(s % 60).padStart(2,'0');
    const mmm = String(msR).padStart(3,'0');
    return `${hh}:${mm}:${ss},${mmm}`;
  };
  return transcript.map((t, i, arr) => {
    const start = Math.round(t.offset);
    const nextStart = arr[i+1]?.offset;
    const duration = t.duration || (nextStart ? nextStart - t.offset : 2000);
    const end = Math.round(t.offset + duration);
    return `${i+1}\n${toTime(start)} --> ${toTime(end)}\n${t.text}\n`;
  }).join('\n').trim() + '\n';
}

exports.handler = async (event) => {
  try {
    const qs = event.queryStringParameters || {};
    const url = qs.video_url || qs.url || '';
    const format = (qs.format || 'txt').trim().toLowerCase(); // txt | srt
    const vid = getYouTubeId(url);

    if (!vid) {
      return { statusCode: 400, body: 'Invalid or missing YouTube URL.' };
    }

    let transcript = null;

    // Önce İngilizce dene
    try {
      transcript = await YoutubeTranscript.fetchTranscript(vid, { lang: 'en' });
    } catch {}

    // Olmazsa en-US dene
    if (!transcript || !transcript.length) {
      try {
        transcript = await YoutubeTranscript.fetchTranscript(vid, { lang: 'en-US' });
      } catch {}
    }

    // Hâlâ yoksa default (otomatik)
    if (!transcript || !transcript.length) {
      try {
        transcript = await YoutubeTranscript.fetchTranscript(vid);
      } catch {}
    }

    if (!transcript || !transcript.length) {
      return { statusCode: 404, body: 'No subtitles found for this video.' };
    }

    // Format seçimi
    let payload, ext;
    if (format === 'srt') {
      payload = toSrt(transcript);
      ext = 'srt';
    } else {
      payload = toTxt(transcript);
      ext = 'txt';
    }

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Disposition': `attachment; filename="subtitles_${vid}.${ext}"`,
        'Cache-Control': 'no-store',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Expose-Headers': 'Content-Disposition'
      },
      body: payload
    };
  } catch (err) {
    console.error('subtitle error', err);
    return { statusCode: 500, body: `Subtitle service error: ${err.message}` };
  }
};
