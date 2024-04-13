<template>
    <div >
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1" style="display: none;">
            <symbol id="wave" viewBox="0 0 560 20">
                <path d="M420,20c21.5-0.4,38.8-2.5,51.1-4.5c13.4-2.2,26.5-5.2,27.3-5.4C514,6.5,518,4.7,528.5,2.7c7.1-1.3,17.9-2.8,31.5-2.7c0,0,0,0,0,0v20H420z"></path>
                <path d="M420,20c-21.5-0.4-38.8-2.5-51.1-4.5c-13.4-2.2-26.5-5.2-27.3-5.4C326,6.5,322,4.7,311.5,2.7C304.3,1.4,293.6-0.1,280,0c0,0,0,0,0,0v20H420z"></path>
                <path d="M140,20c21.5-0.4,38.8-2.5,51.1-4.5c13.4-2.2,26.5-5.2,27.3-5.4C234,6.5,238,4.7,248.5,2.7c7.1-1.3,17.9-2.8,31.5-2.7c0,0,0,0,0,0v20H140z"></path>
                <path d="M140,20c-21.5-0.4-38.8-2.5-51.1-4.5c-13.4-2.2-26.5-5.2-27.3-5.4C46,6.5,42,4.7,31.5,2.7C24.3,1.4,13.6-0.1,0,0c0,0,0,0,0,0l0,20H140z"></path>
            </symbol>
        </svg>
        <div class="box">
            <div class="percent">
                <div class="percentNum">{{ percent }}</div>
                <div class="percentB">%</div>
                
            </div>
            <div class="percent-state">
                <div class="percentNum" v-if="!learning && percent>=60">可 学 习</div>
                <div class="percentNum" v-if="!learning && percent<60">不 可 学 习</div>
                <div class="percentNum" v-if="learning">学 习 中 . . .</div>
            </div>
            <div
                id="water"
                class="water"
                :style="{ transform: 'translate(0,' + (100 - percent) + '%)' }"
            >
                <svg viewBox="0 0 560 20" class="water_wave water_wave_back"  v-if="percent>0">
                    <use xlink:href="#wave" />
                </svg>
                <svg viewBox="0 0 560 20" class="water_wave water_wave_front"  v-if="percent>0">
                    <use xlink:href="#wave" />
                </svg>
            </div>
            <!-- <div
                id="water_line"
                class="water_line"
                :style="{ transform: 'translate(0,' + (100 - 60) + '%)' }"
            >
                <svg viewBox="0 0 560 20" >
                    
                </svg>
            </div> -->
           
        </div>
    </div>
</template>

<script>
import { computed } from 'vue';

export default {
    // data() {
    //     return {
    //         percent: 60,
    //         interval: null
    //     };
    // },
    props:{
        num:{
            type: Number,
            required: true,
        },
        
        learning:{
            type: Boolean,
            required: true,
        },
    },
    mounted() {
        // this.interval = setInterval(() => {
        //     this.percent++;
        //     if (this.percent === 100){
        //         //clearInterval(this.interval);
        //         this.percent=0
        //     } 
        // }, 200);
    },
    beforeDestroy() {
        clearInterval(this.interval);
    },
    setup(props){
        let percent = computed(() => Number(props.num / 100));
        console.log('percent', percent)
        return {
            percent,
        }
    }
};
</script>

<style scoped>
*,
*:before,
*:after {
    box-sizing: border-box;
    outline: none;
}

body {
    -webkit-font-smoothing: antialiased;
}
.waterball-container {
    position: relative; /* 保证它是相对于父组件进行定位 */
}
.box{
    height: 200px;
    width: 200px;
    position: relative; /* 更改这里 */
    top: 60%;
    left: 20%;
    transform: translate(20%, 20%);
    background: #fff;
    border-radius:100%;
    overflow: hidden; 
    box-shadow: 0 0 30px 10px rgba(185, 212, 228, 0.5);  /* 添加了光晕效果 */
}
.percent{
    position: absolute;
    left: 0;
    top: 0;
    z-index:3;
    top: -10%;
    width: 100%;
    height: 100%;
    display: flex;
    align-items:center;
    justify-content:center; 
    color:#000;
    font-size:24px;
    font-weight: bold; /* 加粗字体 */
    font-family: 'Arial'; /* 设定字体 */
} 
.percent-state{
    position: absolute;
    left: 0;
    top: 0;
    z-index:3;
    width: 100%;
    height: 100%;
    top: 10%;
    display: flex;
    align-items:center;
    justify-content:center; 
    color:#766b6b;
    font-size:16px;
    font-family: "Western"; /* 设定字体 */
} 
.water{
    position: absolute;
    left: 0;
    top: 0;
    z-index:2;
    width: 100%;
    height: 100%;
    background:rgb(161, 193, 255);
    transition: all .3s;
}
.water_line {
    position: absolute;
    left: 0;
    top: 0;
    z-index: 2;
    width: 0%;
    height: 0%;
    background: rgba(201, 206, 225, 0.5);
    transition: all .3s;
    box-shadow: 0 0 30px 230px rgba(213, 220, 233, 0.3);  /* 添加了光晕效果 */
}
.water_wave{
    width: 200%;
    position: absolute;
    bottom: 100%;
}
.water_wave_back{
    right: 0;
    fill: #C7EEFF;
    animation: wave-back 1.4s infinite linear;
}
.water_wave_front{
    left: 0;
    fill: rgb(161, 193, 255);
    margin-bottom: -1px;
    animation: wave-front .7s infinite linear;
}
@keyframes wave-front {
    100% {
        transform: translate(-50%, 0);
    }
}
@keyframes wave-back {
    100% {
        transform: translate(50%, 0);
    }
}
</style>