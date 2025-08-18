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

function toTxt(transcript) {
  return transcript.map(t => t.text).join('\n').trim() + '\n';
}

exports.handler = async (event, context) => {
  const url = event.queryStringParameters.url;
  const format = event.queryStringParameters.format || 'txt';
  const videoId = getYouTubeId(url);

  if (!videoId) {
    return { statusCode: 400, body: 'Invalid YouTube URL' };
  }

  try {
    const transcript = await YoutubeTranscript.fetchTranscript(videoId);
    const text = toTxt(transcript);

   return {
  statusCode: 200,
  headers: {
    'Content-Type': 'text/html; charset=utf-8',
    'Content-Disposition': 'inline'   // <<< artık tarayıcıda açar
  },
  body: `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <title>Transcript</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 20px; }
          pre { white-space: pre-wrap; word-wrap: break-word; }
        </style>
      </head>
      <body>
        <h2>YouTube Transcript</h2>
        <pre>${text}</pre>
      </body>
    </html>
  `
};

  } catch (e) {
    return { statusCode: 500, body: e.message };
  }
};
