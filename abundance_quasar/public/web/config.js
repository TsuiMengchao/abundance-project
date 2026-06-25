// 环境检测
const isMobileApp = () => {
    if (window.__NATIVE__ || window.electron || window.uni || window.wx || window.plus) {
                return true;
            }
            return true;
};

// 工具元数据
const tools = [
    { id: 'ip-lookup', name: 'IP 查询', icon: '🌐', desc: '查询IP地理位置', tab: 'online', category: 'dev', component: 'IpLookup' },
    { id: 'timestamp', name: '时间戳转换', icon: '🕒', desc: '时间戳与时区转换', tab: 'offline', category: 'dev', component: 'Timestamp' },
    { id: 'calculator', name: '科学计算器', icon: '🧮', desc: '标准/科学计算', tab: 'offline', category: 'utility', component: 'Calculator' },
    { id: 'unit-convert', name: '单位换算', icon: '📏', desc: '长度/重量/温度/进制', tab: 'offline', category: 'utility', component: 'UnitConvert' },
    { id: 'qrcode-gen', name: '二维码生成', icon: '📱', desc: '离线生成二维码', tab: 'offline', category: 'utility', component: 'QRCodeGen' },
    { id: 'weather', name: '天气查询', icon: '☁️', desc: '实时天气(需联网)', tab: 'online', category: 'utility', component: 'Weather' },
    { id: 'device-info', name: '设备信息', icon: '📖', desc: '离线文本查看', tab: 'offline', category: 'dev', component: 'NativeIFrame', src: 'public/deviceinfo/index.html' },
    { id: 'web-source', name: '网页源码获取', icon: '📖', desc: '离线文本查看', tab: 'offline', category: 'dev', component: 'NativeIFrame', src: 'public/websource/index.html' },
    { id: 'notice', name: '通知自己', icon: '📖', desc: '离线文本查看', tab: 'offline', category: 'utility', component: 'NativeIFrame', src: 'public/notice/index.html' },
    { id: 'wooden-fish', name: '电子木鱼', desc: '点击积攒功德，解压神器', icon: '🪔', tab: 'offline', category: 'leisure', component: 'WoodenFish' },
    { id: 'data-reader', name: '数据阅读器', icon: '📖', desc: '离线文本查看', tab: 'offline', category: 'dev', component: 'NativeIFrame', src: 'public/datareader/index.html' },
    { id: 'entry-reader', name: '词条阅读器', icon: '📖', desc: '离线文本查看', tab: 'offline', category: 'dev', component: 'NativeIFrame', src: 'public/entryreader/index.html' },
    {
        id: 'base64',
        name: 'Base64转换',
        desc: '编码/解码',
        icon: '🔐',
        tab: 'offline',
        category: 'dev',
        component: 'Base64Convert'
    },
    {
        id: 'resume',
        name: '简历',
        desc: '简历',
        icon: '🔐',
        tab: 'offline',
        category: 'dev',
        component: 'NativeIFrame',
        src: 'public/resume/index.html'
    }
];

// 应用端顶层tab配置
const tabsApplication = [
    { key: 'local-offline', label: '本地离线', desc: '内置页面·断网可用' },
    { key: 'local-online', label: '本地联网', desc: '内置页面·需联网' },
    { key: 'cloud-offline', label: '云端离线', desc: '云端加载·可缓存离线' },
    { key: 'cloud-online', label: '云端联网', desc: '云端加载·全程联网' }
];

// 网页端顶层tab配置
const tabsWeb = [
    { key: 'offline', label: '离线工具', desc: '云端加载·可缓存离线' },
    { key: 'online', label: '联网工具', desc: '云端加载·全程联网' }
];

// 二级分类常量
const categories = [
    { id: "dev", name: "开发相关" , "rank":1},
    { id: "leisure", name: "休闲相关" , "rank":1},
    { id: "game", name: "小游戏" , "rank":1},
    { id: "utility", name: "实用工具" , "rank":1}
];

// 组件映射（自动匹配子组件）
const componentMap = {
    IpLookup, Timestamp, Calculator, UnitConvert, QRCodeGen, Weather, WoodenFish, NativeIFrame, Base64Convert
};