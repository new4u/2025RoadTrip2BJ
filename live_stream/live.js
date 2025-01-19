let localStream;
let mediaRecorder;
let currentCamera = 'user';

const videoElement = document.getElementById('localVideo');
const startButton = document.getElementById('startBtn');
const stopButton = document.getElementById('stopBtn');
const switchButton = document.getElementById('switchCameraBtn');
const statsElement = document.getElementById('stats');
const platformInfoElement = document.getElementById('platformInfo');
const danmuContainer = document.getElementById('danmuContainer');
const xiaohongshuButton = document.getElementById('xiaohongshuBtn');
const bilibiliButton = document.getElementById('bilibiliBtn');

const PLATFORMS = {
    XIAOHONGSHU: 'xiaohongshu',
    BILIBILI: 'bilibili'
};

const config = {
    currentPlatform: PLATFORMS.XIAOHONGSHU,
    platforms: {
        [PLATFORMS.XIAOHONGSHU]: {
            name: '小红书',
            rtmpUrl: 'rtmp://your-xiaohongshu-rtmp-url',
            streamKey: 'your-xiaohongshu-stream-key'
        },
        [PLATFORMS.BILIBILI]: {
            name: '哔哩哔哩',
            rtmpUrl: 'rtmp://your-bilibili-rtmp-url',
            streamKey: 'your-bilibili-stream-key'
        }
    }
};

// 平台切换
function switchPlatform(platform) {
    console.log('切换平台到:', platform);
    config.currentPlatform = platform;
    updatePlatformUI();
    updatePlatformInfo();
}

function updatePlatformUI() {
    console.log('更新UI, 当前平台:', config.currentPlatform);
    xiaohongshuButton.classList.remove('active');
    bilibiliButton.classList.remove('active');
    
    if (config.currentPlatform === PLATFORMS.XIAOHONGSHU) {
        xiaohongshuButton.classList.add('active');
    } else if (config.currentPlatform === PLATFORMS.BILIBILI) {
        bilibiliButton.classList.add('active');
    }
}

function updatePlatformInfo() {
    const platform = config.platforms[config.currentPlatform];
    platformInfoElement.textContent = `当前平台: ${platform.name}`;
}

async function initializeStream() {
    try {
        localStream = await navigator.mediaDevices.getUserMedia({
            video: { 
                facingMode: currentCamera,
                width: { ideal: 1920 },
                height: { ideal: 1080 }
            },
            audio: true
        });
        videoElement.srcObject = localStream;
        updateStats(); // 初始化后立即更新状态
    } catch (err) {
        console.error('获取摄像头失败:', err);
        alert('无法访问摄像头，请确保已授予权限');
    }
}

async function switchCamera() {
    if (localStream) {
        localStream.getTracks().forEach(track => track.stop());
    }
    currentCamera = currentCamera === 'user' ? 'environment' : 'user';
    await initializeStream();
}

function startLiveStream() {
    if (!localStream) {
        alert('请先允许摄像头访问');
        return;
    }

    const platform = config.platforms[config.currentPlatform];
    if (!platform.rtmpUrl || !platform.streamKey) {
        alert('请先配置直播推流地址和密钥');
        return;
    }

    // 使用WebRTC和RTMP推流
    const pc = new RTCPeerConnection();
    localStream.getTracks().forEach(track => pc.addTrack(track, localStream));
    
    pc.createOffer()
        .then(offer => pc.setLocalDescription(offer))
        .then(() => {
            // 这里需要实现与流媒体服务器的连接
            console.log('开始推流到:', platform.name);
            console.log('推流地址:', platform.rtmpUrl);
            console.log('推流密钥:', platform.streamKey);
        })
        .catch(err => {
            console.error('推流失败:', err);
            alert('推流失败，请检查网络连接');
        });

    startButton.disabled = true;
    stopButton.disabled = false;
    updateStats();
}

function stopLiveStream() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
    }
    startButton.disabled = false;
    stopButton.disabled = true;
}

function updateStats() {
    if (!localStream) return;
    
    const videoTrack = localStream.getVideoTracks()[0];
    const settings = videoTrack.getSettings();
    
    statsElement.textContent = `
        分辨率: ${settings.width}x${settings.height}
        帧率: ${settings.frameRate}
        摄像头: ${currentCamera === 'user' ? '前置' : '后置'}
        平台: ${config.platforms[config.currentPlatform].name}
    `;
}

// 模拟弹幕效果
function createDanmu(text) {
    const danmu = document.createElement('div');
    danmu.className = 'danmu';
    danmu.textContent = text;
    danmu.style.top = Math.random() * 70 + '%';
    danmuContainer.appendChild(danmu);
    
    danmu.addEventListener('animationend', () => {
        danmuContainer.removeChild(danmu);
    });
}

// 测试弹幕
setInterval(() => {
    const messages = ['好看！', '主播加油！', '前方路况如何？', '车子性能真好', '路况不错呀'];
    createDanmu(messages[Math.floor(Math.random() * messages.length)]);
}, 3000);

// 事件监听
startButton.addEventListener('click', startLiveStream);
stopButton.addEventListener('click', stopLiveStream);
switchButton.addEventListener('click', switchCamera);
xiaohongshuButton.addEventListener('click', () => {
    console.log('点击小红书按钮');
    switchPlatform(PLATFORMS.XIAOHONGSHU);
});
bilibiliButton.addEventListener('click', () => {
    console.log('点击B站按钮');
    switchPlatform(PLATFORMS.BILIBILI);
});

// 初始化
initializeStream();
updatePlatformUI();
updatePlatformInfo();
