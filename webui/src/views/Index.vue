<template>
  <div class="wrapper">
    <a-row>
      <a-col :lg="10" :md="10" :sm="9">
        <div class="left-wrapper">
          <!-- <div class="up-img-wrapper"> -->
          <!-- :beforeUpload="beforeUpload" -->
          <div class="upimg-dragger">
            <a-upload-dragger
              name="file"
              action="/tools/ocr_text/"
              @change="handleChange"
              accept=".jpg, .jpeg, .png, .gif, .ico"
              :beforeUpload="beforeUpload"
              listType="picture"
              :showUploadList="false"
            >
              <p>点击、拖动、或者粘贴图片</p>
            </a-upload-dragger>
          </div>
          <div class="up-img-preview">
            <!--  -->
            <img :src="upImage" alt="预览图片" :hidden="previewImgHidden" />
          </div>
          <!-- </div> -->

          <div class="upimg-dragger">
            <a-upload-dragger
              name="file"
              action="/tools/ocr_text/"
              @change="handleLabelLocationPicChange"
              accept=".jpg, .jpeg, .png, .gif, .ico"
              :beforeUpload="beforeUpload"
              listType="picture"
              :showUploadList="false"
            >
              <p>点击、拖动、或者粘贴图片</p>
            </a-upload-dragger>
          </div>
          <div class="up-img-preview">
            <!--  -->
            <img :src="upLocationImage" alt="预览图片" :hidden="previewLocationImgHidden" />
          </div>

        </div>

        
      </a-col>

      <a-col :lg="3" :md="4" :sm="6">
        <div class="split">
          <div class="divider"></div>
          <div class="btn-group">
            <a-button @click="handleUpload" :loading="isOCRing">识别</a-button>
            <a-button @click="handleUploadSave" :loading="isOCRing">识别并存储</a-button>
            <a-button @click="handleUploadDiff" :loading="isOCRDiffing">识别并比较</a-button>
            <a-button @click="getImgList" :loading="isOCRing">获取图片列表</a-button>
            <!-- 压缩图片、显示检测后的图片、显示原始值、显示纯文字 -->
            <div style="margin-top:1rem;">
              <p>
                选择标签位置:
                <a-select default-value="加拿大安全认证_左B柱侧面上方" style="width: 220px" @change="handleLabelLocationChange">
                 <a-select-option value="加拿大安全认证_左B柱侧面上方">
                  加拿大安全认证_左B柱侧面上方
                 </a-select-option>
                 <a-select-option value="北美Loose Item_左侧后三角窗后部">
                  北美Loose Item_左侧后三角窗后部
                 </a-select-option>
                 <a-select-option value="三角窗标签_左侧三角窗">
                  三角窗标签_左侧三角窗
                 </a-select-option>
                 <a-select-option value="北美安全认证_左B柱侧面上方">
                  北美安全认证_左B柱侧面上方
                 </a-select-option>
                 <a-select-option value="北美胎压_左侧B柱侧面下方">
                  北美胎压_左侧B柱侧面下方
                 </a-select-option>
                 <a-select-option value="加拿大安全警示标签_右前车门玻璃内侧">
                  加拿大安全警示标签_右前车门玻璃内侧
                 </a-select-option>
                 <a-select-option value="中东燃油排放消耗标识_右后车门玻璃内侧">
                  中东燃油排放消耗标识_右后车门玻璃内侧
                 </a-select-option>
                 <a-select-option value="加注指示标识_油箱盖内">
                  加注指示标识_油箱盖内
                 </a-select-option>
                 <a-select-option value="国内燃油排放消耗标识_前挡右上方">
                  国内燃油排放消耗标识_前挡右上方
                 </a-select-option>
                </a-select>
              </p>
              <p>
                选择模型:
                <a-select default-value="dataelem" style="width: 220px" @change="handleOrcModelChange">
                 <a-select-option value="huawei">
                   华为
                 </a-select-option>
                 <a-select-option value="baidu">
                   百度
                 </a-select-option>
                 <a-select-option value="dataelem">
                   数据项素
                 </a-select-option>
                </a-select>
              </p>
              <p>
                选择检测语言:
                <a-select default-value="en" style="width: 220px" @change="handleLanguageChange">
                 <a-select-option value="en">
                   英文
                 </a-select-option>
                 <a-select-option value="ch">
                   中文
                 </a-select-option>
                </a-select>
              </p>
              <p>
                压缩图片:
                <a-switch
                  style="width:auto;min-width:45%;"
                  checked-children="开"
                  un-checked-children="关"
                  default-checked
                  @change="changeCompressBtn"
                />
              </p>
              <p :hidden="hiddenCompressBox">
                压缩尺寸:
                <a-input-number
                  style="width:auto;max-width:45%;"
                  id="compressSizeInput"
                  size="small"
                  v-model="comporessSize"
                  :min="1"
                />
                <!-- @change="onChange" -->
              </p>
              <p>
                置信度大于:
                <a-input-number
                  style="width:auto;max-width:45%;"
                  id="confidenceInput"
                  size="small"
                  v-model="confidence"
                  :min="0"
                />
                <!-- @change="onChange" -->
              </p>
              <p>
                标签提取模式:
                <a-switch
                  style="width:auto;min-width:45%;"
                  checked-children="开"
                  un-checked-children="关"
                  default-un-checked
                  @change="changeLabelExtractBtn"
                />
              </p>
            </div>
          </div>

        </div>
      </a-col>

      <a-col :lg="11" :md="10" :sm="9">
        <div class="right-wrapper">
          <div class="detected-img" :hidden="hiddenDetectedImg">
            <a-divider orientation="left">文字检测结果</a-divider>

            <img :src="detectedImg" alt="检测结果图片" />
          </div>

          <div class="ocr-raw" :hidden="hiddenOcrRaw">
            <a-divider orientation="left">原始结果</a-divider>
            <CodeHighlight :txt="ocrRaw" />
          </div>

          <div class="ocr-text" :hidden="hiddenOcrText">
            <a-divider orientation="left">识别的文字</a-divider>
            <CodeHighlight :txt="ocrText" />
          </div>
        </div>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import Vue from 'vue'

const axios = require('axios')
import CodeHighlight from '../components/CodeHighlight.vue'
import Message from 'ant-design-vue'
Vue.use(Message)

// 获取上传对象的临时链接
function getObjectURL(file) {
  var url = null
  if (window.createObjectURL != undefined) {
    url = window.createObjectURL(file)
  } else if (window.URL != undefined) {
    // mozilla(firefox)
    url = window.URL.createObjectURL(file)
  } else if (window.webkitURL != undefined) {
    // webkit or chrome
    url = window.webkitURL.createObjectURL(file)
  }
  return url
}

export default {
  name: 'Index',
  data: function() {
    return {
      upImage: '', // 上传后的图片预览地址
      upLocationImage: '', // 标签位置上传后的图片预览地址
      fileList: [], // 上传图片的列表
      detectedImg: '', // 检测后的图片
      ocrRaw: ``, // 返回的原始结果
      ocrText: ``, // 经过提取后的文字结果

      uploading: false, //状态 原生 上传控件的状态
      previewImgHidden: true, // 状态 预览图片是否隐藏
      previewLocationImgHidden: true, // 状态 标签位置预览图片是否隐藏
      isOCRing: false, // 状态 是否在识别中
      isOCRDiffing: false,
      hiddenDetectedImg: true, //状态  是否显示检测后的图片
      hiddenOcrRaw: true, // 状态  是否显示返回的原始结果
      hiddenOcrText: true, // 状态 是否显示经过提取后的文字结果
      comporessSize: 1600,
      confidence: 0, // 置信度
      ocrModel: 'dataelem',
      language: 'en',
      hiddenCompressBox:false,
      labelExtract:false
    }
  },
  components: {
    CodeHighlight
  },
  methods: {
    handleOrcModelChange(value) {
      this.ocrModel = value
    },
    handleLanguageChange(value) {
      this.language = value
    },
    changeCompressBtn(checked) {

      if(checked === true){
        this.$data.hiddenCompressBox = false
      }
      else{
        this.$data.hiddenCompressBox = true
      }
    },
    changeLabelExtractBtn(checked) {

      if(checked === false){
        this.$data.labelExtract = false
      }
      else{
        this.$data.labelExtract = true
      }
    },
    handleChange(info) {
      const status = info.file.status
      if (status !== 'uploading') {
        // this.$data.fileList = [info.file]
        this.$data.fileList.push(info.file)
        this.$data.upImage = getObjectURL(info.file)
        this.$data.previewImgHidden = false
        console.log('success')
      }
      if (status === 'done') {
        console.log('done')
        this.$message.success(`${info.file.name} file uploaded successfully.`)
      } else if (status === 'error') {
        this.$message.error(`${info.file.name} file upload failed.`)
        console.log('error')
      }
    },
    handleLabelLocationPicChange(info) {
      const status = info.file.status
      if (status !== 'uploading') {
        // this.$data.fileList = [info.file]
        this.$data.fileList.push(info.file)
        this.$data.upLocationImage = getObjectURL(info.file)
        this.$data.previewLocationImgHidden = false
        console.log('success')
      }
      if (status === 'done') {
        console.log('done')
        this.$message.success(`${info.file.name} file uploaded successfully.`)
      } else if (status === 'error') {
        this.$message.error(`${info.file.name} file upload failed.`)
        console.log('error')
      }
    },
    beforeUpload(file) {
      // this.fileList = [file]
      // this.fileList.push(file)
      file
      return false
    },
    handleUpload() {
      if (this.fileList.length < 1) {
        this.$message.warning('还没有选择图片')
        return
      }
      console.log(this.fileList.length)
      const formData = new FormData()
      this.fileList.forEach(file => {
        formData.append('img_upload', file)
      })
      if (this.$data.hiddenCompressBox === true){
        formData.append('compress_size',0)
      }else{
        formData.append('compress_size',this.$data.comporessSize)
      }
      formData.append('ocr_model',this.$data.ocrModel)
      formData.append('confidence',this.$data.confidence)
      formData.append('language',this.$data.language)
      console.log(this.$data.ocrModel)
      this.isOCRing = true
      this.uploading = true

      const _this = this

      this.$data.fileList = []
      axios({
        url: '/api/ocr',
        method: 'post',
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-Requested-With': 'XMLHttpRequest'
        },
        transformRequest: {},
        data: formData
      })
        .then(function(response) {
          _this.$data.detectedImg = response.data['data']['img_detected']

          _this.$data.ocrRaw = ''
          _this.$data.ocrText = ''

          let nextLineHeight = 0 // 下一行的高度

          const raw_data = response.data['data']['raw_out']
          for (let i = 0; i < raw_data.length; i++) {
            _this.$data.ocrRaw += JSON.stringify(raw_data[i]) + '\r'

            // 合并同一行的数据
            if (i < raw_data.length - 1) {
              nextLineHeight = raw_data[i + 1][0][1]
              // 判断判断同一行的依据是 两段的行高差 小于 行高的一半
              if (
                Math.abs(raw_data[i][0][1] - nextLineHeight) <
                raw_data[i][0][3] / 2
              ) {
                _this.$data.ocrText += raw_data[i][1] + ' '
              } else {
                _this.$data.ocrText += raw_data[i][1] + '\r'
              }
            } else {
              _this.$data.ocrText += raw_data[i][1]
            }

            // _this.$data.ocrText += raw_data[i][1] + '\r'
          }

          _this.$data.uploading = false
          _this.$data.isOCRing = false
          _this.$data.hiddenDetectedImg = false
          _this.$data.hiddenOcrRaw = false
          _this.$data.hiddenOcrText = false

          _this.$message.success(
            '成功! 耗时：' + response.data['data']['speed_time'] + ' 秒'
          )
        })
        .catch(function(error) {
          // console.log(error)
          _this.$data.isOCRing = false

          const errorInfo = error.response['msg'] || error.message
          _this.$message.error('错误：' + errorInfo)

          _this.$data.hiddenDetectedImg = true
          _this.$data.hiddenOcrRaw = true
          _this.$data.hiddenOcrText = true
        })
    },
    handleUploadSave() {
      if (this.fileList.length < 1) {
        this.$message.warning('还没有选择图片')
        return
      }
      console.log(this.fileList.length)
      const formData = new FormData()
      this.fileList.forEach(file => {
        formData.append('img_upload', file)
      })
      if (this.$data.hiddenCompressBox === true){
        formData.append('compress_size',0)
      }else{
        formData.append('compress_size',this.$data.comporessSize)
      }
      formData.append('confidence',this.$data.confidence)
      formData.append('ocr_model',this.$data.ocrModel)
      formData.append('vin','5LMPJ8KA7RJ739205')
      formData.append('language',this.$data.language)

      this.isOCRing = true
      this.uploading = true

      const _this = this

      this.$data.fileList = []
      axios({
        url: '/api/save',
        method: 'post',
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-Requested-With': 'XMLHttpRequest'
        },
        transformRequest: {},
        data: formData
      })
        .then(function(response) {
          _this.$data.detectedImg = response.data['data']['img_detected']

          _this.$data.ocrRaw = ''
          _this.$data.ocrText = ''

          let nextLineHeight = 0 // 下一行的高度

          const raw_data = response.data['data']['raw_out']
          for (let i = 0; i < raw_data.length; i++) {
            _this.$data.ocrRaw += JSON.stringify(raw_data[i]) + '\r'

            // 合并同一行的数据
            if (i < raw_data.length - 1) {
              nextLineHeight = raw_data[i + 1][0][1]
              // 判断判断同一行的依据是 两段的行高差 小于 行高的一半
              if (
                Math.abs(raw_data[i][0][1] - nextLineHeight) <
                raw_data[i][0][3] / 2
              ) {
                _this.$data.ocrText += raw_data[i][1] + ' '
              } else {
                _this.$data.ocrText += raw_data[i][1] + '\r'
              }
            } else {
              _this.$data.ocrText += raw_data[i][1]
            }

            // _this.$data.ocrText += raw_data[i][1] + '\r'
          }

          _this.$data.uploading = false
          _this.$data.isOCRing = false
          _this.$data.hiddenDetectedImg = false
          _this.$data.hiddenOcrRaw = false
          _this.$data.hiddenOcrText = false

          _this.$message.success(
            '成功! 耗时：' + response.data['data']['speed_time'] + ' 秒'
          )
        })
        .catch(function(error) {
          // console.log(error)
          _this.$data.isOCRing = false

          const errorInfo = error.response['msg'] || error.message
          _this.$message.error('错误：' + errorInfo)

          _this.$data.hiddenDetectedImg = true
          _this.$data.hiddenOcrRaw = true
          _this.$data.hiddenOcrText = true
        })
    },
    handleUploadDiff() {
      if (this.fileList.length < 1) {
        this.$message.warning('还没有选择图片')
        return
      }
      console.log(this.fileList.length)
      const formData = new FormData()
      this.fileList.forEach(file => {
        formData.append('img_upload', file)
      })
      if (this.$data.hiddenCompressBox === true){
        formData.append('compress_size',0)
      }else{
        formData.append('compress_size',this.$data.comporessSize)
      }
      formData.append('confidence',this.$data.confidence)
      formData.append('ocr_model',this.$data.ocrModel)
      formData.append('id',5)
      formData.append('label_extract',this.$data.labelExtract)

      this.isOCRDiffing = true
      this.uploading = true

      const _this = this

      this.$data.fileList = []
      axios({
        url: '/api/diff',
        method: 'post',
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-Requested-With': 'XMLHttpRequest'
        },
        transformRequest: {},
        data: formData
      })
        .then(function(response) {
          _this.$data.detectedImg = response.data['data']['img_detected']

          _this.$data.ocrRaw = response.data['code']
          _this.$data.ocrText = ''
          

          // let nextLineHeight = 0 // 下一行的高度

          // const raw_data = response.data['data']['raw_out']
          // for (let i = 0; i < raw_data.length; i++) {
          //   _this.$data.ocrRaw += JSON.stringify(raw_data[i]) + '\r'

          //   // 合并同一行的数据
          //   if (i < raw_data.length - 1) {
          //     nextLineHeight = raw_data[i + 1][0][1]
          //     // 判断判断同一行的依据是 两段的行高差 小于 行高的一半
          //     if (
          //       Math.abs(raw_data[i][0][1] - nextLineHeight) <
          //       raw_data[i][0][3] / 2
          //     ) {
          //       _this.$data.ocrText += raw_data[i][1] + ' '
          //     } else {
          //       _this.$data.ocrText += raw_data[i][1] + '\r'
          //     }
          //   } else {
          //     _this.$data.ocrText += raw_data[i][1]
          //   }

          //   // _this.$data.ocrText += raw_data[i][1] + '\r'
          // }

          _this.$data.uploading = false
          _this.$data.isOCRDiffing = false
          _this.$data.hiddenDetectedImg = false
          _this.$data.hiddenOcrRaw = false
          _this.$data.hiddenOcrText = false

          _this.$message.success(
            '成功! 耗时：' + response.data['data']['speed_time'] + ' 秒'
          )
        })
        .catch(function(error) {
          // console.log(error)
          _this.$data.isOCRing = false
          _this.$data.isOCRDiffing = false
          const errorInfo = error.response['msg'] || error.message
          _this.$message.error('错误：' + errorInfo)

          _this.$data.hiddenDetectedImg = true
          _this.$data.hiddenOcrRaw = true
          _this.$data.hiddenOcrText = true
        })
    },
    getImgList() {
     
      const formData = new FormData()


      formData.append('vin','5LMPJ8KA7RJ739205')

      this.isOCRing = true
      this.uploading = true

      const _this = this

      axios({
        url: '/api/images',
        method: 'post',
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-Requested-With': 'XMLHttpRequest'
        },
        transformRequest: {},
        data: formData
      })
        .then(function(response) {
          _this.$data.detectedImg = response.data['data']['images'][0]['label_img']

          _this.$data.ocrRaw = ''
          _this.$data.ocrText = ''

          _this.$data.uploading = false
          _this.$data.isOCRing = false
          _this.$data.hiddenDetectedImg = false
          _this.$data.hiddenOcrRaw = false
          _this.$data.hiddenOcrText = false

          _this.$message.success(
            '成功! 耗时：' + response.data['data']['speed_time'] + ' 秒'
          )
        })
        .catch(function(error) {
          // console.log(error)
          _this.$data.isOCRing = false

          const errorInfo = error.response['msg'] || error.message
          _this.$message.error('错误：' + errorInfo)

          _this.$data.hiddenDetectedImg = true
          _this.$data.hiddenOcrRaw = true
          _this.$data.hiddenOcrText = true
        })
    },

  },
  
  watch: {
    fileList: function(newVal, oldVal) {
      if (newVal.length <= 0) {
        this.hiddenDetectedImg = true
        this.hiddenOcrRaw = true
        this.hiddenOcrText = true

        oldVal
      }

    }
  },
  mounted: function() {
    // console.log('mounted')
    this.$nextTick(function() {
      // Code that will run only after the
      // entire view has been rendered

      const _this = this
      document.addEventListener('paste', function(event) {
        var items = event.clipboardData && event.clipboardData.items
        var file = null
        if (items && items.length) {
          // 检索剪切板items
          for (var i = 0; i < items.length; i++) {
            if (items[i].type.indexOf('image') !== -1) {
              file = items[i].getAsFile()
              break
            }
          }
        }

        // console.log(file)
        if (file !== null) {
          _this.$data.fileList = [file]
          _this.$data.upImage = getObjectURL(file)
          _this.$data.previewImgHidden = false
        }
        console.log(_this.$data.fileList)
        // 此时file就是剪切板中的图片文件
      })
    })
  }
}
</script>

<style >
/* >>>>>>  覆盖原生样式 */
.ant-divider-inner-text {
  font-size: 14px;
  color: gray;
}

/* <<<<<<  覆盖原生样式 */

.wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  min-height: 100%;
  height: auto;
}
.left-wrapper {
  min-height: 100vh;
  height: auto;
}
.upimg-dragger {
  height: 4rem;
  margin: 2.5rem 0 1rem 2.5rem;
}
.up-img-preview {
  text-align: center;

  margin: 1.5rem -1rem 1rem 1rem;
}
.up-img-preview img {
  object-fit: contain;
  max-width: 95%;
  max-height: 80vh;
}
.split {
  min-height: 100%;
  /* border: solid gray 1px; */
  height: 100vh;
  position: relative;
}
.divider {
  position: absolute;
  left: 50%;
  top: 0;
  min-height: 100%;
  height: auto;
  width: 1px;
  border-left: 1px solid #d3d3d36b;
}
.btn-group {
  text-align: center;
  margin: 2.5rem 0;
  padding: 1rem;
  background: white;
  width: 100%;
  position: absolute;
}
.btn-group button {
  width: 90%;
}
.right-wrapper {
  padding: 1rem 2.5rem 1rem 0;
}

.detected-img {
  max-height: 50%;
  /* border: 1px solid gray; */
  text-align: center;
}
.detected-img img {
  object-fit: contain;
  max-width: 100%;
  max-height: 40vh;
}
.detected-img .ocr-raw {
  max-height: 40vh;
}
.detected-img .ocr-text {
  max-height: 40vh;
}
</style>
