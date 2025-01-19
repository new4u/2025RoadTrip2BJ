// 直播平台配置
const PLATFORMS = {
    XIAOHONGSHU: 'xiaohongshu',
    BILIBILI: 'bilibili'
};

const config = {
    currentPlatform: PLATFORMS.XIAOHONGSHU,  // 默认使用小红书
    platforms: {
        [PLATFORMS.XIAOHONGSHU]: {
            name: '小红书',
            rtmpUrl: '',  // 需要填入您的小红书直播推流地址
            streamKey: '' // 需要填入您的直播密钥
        },
        [PLATFORMS.BILIBILI]: {
            name: 'Bilibili',
            rtmpUrl: '',  // 需要填入您的B站直播推流地址
            streamKey: '' // 需要填入您的直播密钥
        }
    }
};
