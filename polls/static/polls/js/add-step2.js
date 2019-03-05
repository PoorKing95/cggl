var form2 = new Vue({
    el: "#form2",
    data: {
        showList: false,
        keyword: '',
        optionList: [],
        select: -1,
        authors: authors,
    },
    watch: {
        keyword: function(newKeyword, oldKeyword) {
            this.showOptionList()
        },
    },
    methods: {
        showOptionList: function() {
            if (this.keyword == this.getName(this.select) && this.keyword != '') {
                return
            }

            if (/^\s+$/.test(this.keyword) || this.keyword == '') {
                this.showList = false
                return
            }
            this.select = -1
            // this.updateOptionList()
            // this.showList = true

            let _this = this
            axios.get('/polls/author-list', {
                params: {
                    prefix: this.keyword
                }
            }).then(resp => {
                let options = []
                for (let i = 0; i < resp.data.length; i++) {
                    options.push({select: false, val: resp.data[i]})
                }
                _this.optionList = options
                _this.showList = true
            }).catch(err => {
                _this.showList = false
            })
        },
        selectItem: function(i) {
            this.setItem(this.select, false)
            this.setItem(i, true)
        },
        setItem: function(i, flag) {
            if (i < 0 || i >= this.optionList.length) {
                return
            }

            this.select = flag ? i : -1
            this.optionList[i].select = flag
        },
        lastItem: function() {
            if (!this.showList) {
                return
            }
            var index = this.select
            this.setItem(index, false)

            index -= 1
            if (index < 0) {
                index = this.optionList.length - 1
            }
            this.setItem(index, true)
            this.keyword = this.getName(index)
        },
        nextItem: function() {
            if (!this.showList) {
                return
            }
            var index = this.select
            this.setItem(index, false)

            index += 1
            if (index >= this.optionList.length) {
                index = 0
            }
            this.setItem(index, true)
            this.keyword = this.getName(index)
        },
        getName: function(i) {
            if (i < 0 || i >= this.optionList.length) {
                return ''
            }
            return this.optionList[i].val.anamech
        },
        addAuthor: function() {
            if (this.select == -1) {
                if (this.authors.length == 0) {
                    return
                }

                if (this.optionList[0].val.anamech == this.keyword) {
                    this.authors.push(this.optionList[0].val)
                    this.keyword = ''
                    return
                }
                alert("not found")
            }
            this.keyword = ''
            let author = this.optionList[this.select].val
            for (let i = 0; i < this.authors.length; i++) {
                if (author.amail === this.authors[i].amail) {
                    alert("该作者已经添加")
                    return
                }
            }
            this.authors.push(this.optionList[this.select].val)
        },
        delAuthor: function(mail) {
            this.authors = this.authors.filter(author => {
                return author.amail != mail
            })
        },
        onSave: function () {
            let _this = this
            axios.post('/polls/add-authors', _this.authors).then(resp => {
                if (resp.data.success) {
                    window.location = '/polls/add-step3'
                } else {
                    alert(resp.data.message)
                }
            }).catch(err => {

            });
        }
    }
});