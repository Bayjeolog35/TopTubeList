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

exports.handler = async (event) => {
  try {
    const { url, format } = event.queryStringParameters;
    const videoId = getYouTubeId(url);
    if (!videoId) {
      return { statusCode: 400, body: 'Invalid YouTube URL' };
    }

    const transcript = await YoutubeTranscript.fetchTranscript(videoId);

    let body = toTxt(transcript);
    let contentType = "text/plain";

    // content-disposition kaldırıldı, download zorunlu değil
    return {
      statusCode: 200,
      headers: { "Content-Type": contentType },
      body,
    };
  } catch (err) {
    return { statusCode: 500, body: err.toString() };
  }
};
