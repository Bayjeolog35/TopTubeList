// netlify/functions/download-subtitles.js
const { YoutubeTranscript } = require('youtube-transcript');

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

function toTxt(transcript) {
  // transcript: [{text, offset, duration}]
  return transcript.map(t => t.text).join('\n').trim() + '\n';
}

function toSrt(transcript) {
  const toTime = ms => {
    const s = Math.floor(ms / 1000), msR = ms % 1000;
    const hh = String(Math.floor(s / 3600)).padStart(2, '0');
    const mm = String(Math.floor((s % 3600) / 60)).padStart(2, '0');
    const ss = String(s % 60).padStart(2, '0');
    const mmm = String(msR).padStart(3, '0');
    return `${hh}:${mm}:${ss},${mmm}`;
  };

  return transcript.map((t, i) => {
    const start = toTime(t.offset);
    const end = toTime(t.offset + t.duration);
    return `${i + 1}\n${start} --> ${end}\n${t.text}\n`;
  }).join('\n');
}

exports.handler = async (event) => {
  try {
    const { url, format } = event.queryStringParameters || {};
    if (!url) {
      return {
        statusCode: 400,
        body: 'Missing YouTube URL ?url=...'
      };
    }

    const videoId = getYouTubeId(url);
    if (!videoId) {
      return {
        statusCode: 400,
        body: 'Invalid YouTube URL'
      };
    }

    const transcript = await YoutubeTranscript.fetchTranscript(videoId);
    if (!transcript || transcript.length === 0) {
      return {
        statusCode: 404,
        body: 'Transcript not available'
      };
    }

    let text;
    if (format === 'srt') {
      text = toSrt(transcript);
    } else {
      text = toTxt(transcript);
    }

    // HTML içinde inline gösterim
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
        'Content-Disposition': 'inline'
      },
      body: `
        <!DOCTYPE html>
        <html>
          <head>
            <meta charset="UTF-8">
            <title>YouTube Transcript</title>
            <style>
              body { font-family: Arial, sans-serif; padding: 20px; line-height: 1.5; background: #fafafa; }
              pre { white-space: pre-wrap; word-wrap: break-word; }
            </style>
          </head>
          <body>
            <h2>Transcript (${format || 'txt'})</h2>
            <pre>${text}</pre>
          </body>
        </html>
      `
    };

  } catch (err) {
    return {
      statusCode: 500,
      body: 'Error: ' + err.message
    };
  }
};
