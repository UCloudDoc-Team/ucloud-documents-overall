/**
 * Created by lenovo on 2017/3/17.
 */
$(document).ready(function(){
    function generatStru (ctx){
    var generatHtmlChild = '';
     $.each(ctx,function(){ 
         generatHtmlChild +='<li class="wflowBox"><div class="pd_sort_head">'+this.listname+'</div><ul>';
         $.each(this.listvalue,function(){
            generatHtmlChild +='<li><a href="'+this.links+'">'+this.name+'</a></li>';
         }) 
         generatHtmlChild +='</ul></li>';    
     })
     return generatHtmlChild;
    };
    //导航内容生成
    $.ajax({
        type:"GET",
        url:"/nav.json",
        cache: false,
        dataType:"json",
        success:function(data){
            var pdList = data.pd;
            var pdHotprods = data.hotprods;
            var pdgethtml = generatStru(pdList);
            var pdHotprodshtml = generatHotprods(pdHotprods);
            $("#pd .wrap_pd_list .enterbox").html(pdgethtml);
            $("#pd .nav-hotprods .nmain").html(pdHotprodshtml);
        }
    });
    $.ajax({
        type:"GET",
        url:"/api/apinav.json",
        cache: false,
        dataType:"json",
        success:function(data){
            var apiList = data.api;
            var apiHotprods = data.hotprods;
            var apigethtml = generatStru(apiList);
            var apiHotprodshtml = generatHotprods(apiHotprods);
            $("#api .wrap_pd_list .enterbox").html(apigethtml);
            $("#api .nav-hotprods .nmain").html(apiHotprodshtml);
        }
    });
    function generatHotprods (ctx){
                    var generatHtmlChild = '';
                        $.each(ctx,function(){ 
                            generatHtmlChild +='<a class="hotprods" target="_blank" href="'+this.url+'"><p class="title">'+this.title+'</p><p class="des">'+this.des+'</p></a>'; 
                        })
                    return generatHtmlChild;
    };
    function generatStru (ctx){
                    var generatHtmlChild = '';
                        $.each(ctx,function(){ 
                            generatHtmlChild +='<li class="wflowBox"><div class="pd_sort_head">'+this.listname+'</div><ul>';
                            $.each(this.listvalue,function(){
                                generatHtmlChild +='<li><a href="'+this.links+'">'+this.name+'</a></li>';
                            }) 
                            generatHtmlChild +='</ul></li>';    
                        })
                    return generatHtmlChild;
    };
    //导航下拉菜单
    (function($) {
        var TopMenu = {
            $wrapper: $('.docs-header'),

            $toggles: $('#topmenu>.submenu'),

            $subMenus: $('#menudropdowns>.nav-menu-dropdown>.nav-menu-wrap'),

            timer: null,

            delay: 100,

            //获取对应dropdown
            getSub: function ($toggle) {
                return $('#' + $toggle.data('href')).find('.nav-menu-wrap').eq(0);
            },

            addClassOnly: function ($ele, classname) {
                return $ele.addClass(classname).siblings().removeClass(classname);
            },

            //导航定位
            navLocation:function () {
                var visitURL = window.location.pathname.split('/')[1];
                if($.trim(visitURL) == $.trim('api')){
                    $('#topmenu>li').each(function(){
                        var name = $(this).data('href');
                        if($.trim(name) == $.trim('api')){
                            $(this).addClass('selected').siblings().removeClass('selected');
                            return false;
                        }
                    });
                }else{
                   $('#topmenu>li:first-child').addClass('selected').siblings().removeClass('selected');
                }
            },

            //瀑布流布局
            arrangement:function(box,boxContent){
                var listwidth = box.eq(0).outerWidth(true)? box.eq(0).outerWidth(true): 242;
                var dockerwidth = $('.docs-header .wrap_pd_list .nmain').eq(0).width() > $('.docs-header .wrap_pd_list .nmain').eq(1).width() ? $('.docs-header .wrap_pd_list .nmain').eq(0).width() : $('.docs-header .wrap_pd_list .nmain').eq(1).width();
                var num = Math.floor(dockerwidth / listwidth),
                    columnHeightArr = [];
                if(listwidth >= 242){
                    if((dockerwidth - listwidth * num - listwidth + 40) >= 0){
                    num = num+1;
                    }
                }
                if(num >=1 && num <=3){
                columnHeightArr.length = num;
                box.each(function(index,item){
                    if (index < num) {
                        if(index == 0){
                            $(item).css({"position":"relative","top":0,"left":0});
                        }else{
                            $(item).css({"position":"relative","top":0,"left":0,"width":listwidth - 40 + "px"});
                        }
        　　　　         columnHeightArr[index] = $(item).position().top + $(item).outerHeight(true);
        　　         } else {
        　　　　         var minHeight = Math.min.apply(null, columnHeightArr),
                        minHeightIndex = $.inArray(minHeight, columnHeightArr);
        　　　　         $(item).css({
               　　         position: 'absolute',
               　　         top: minHeight,
               　　         left: box.eq(minHeightIndex).position().left,
                            width : listwidth - 40 + "px"
                        });
        　　　　         columnHeightArr[minHeightIndex] += $(item).outerHeight(true);
        　　         }
                })
                boxContent.css('minHeight',Math.max.apply(null, columnHeightArr));
                }
            },

            //判断字符串结尾字符
            strEndWith:function ( str,icon) {
                var d = str.length - icon.length;
                return (d>=0 && str.lastIndexOf(icon)==d);
            },

            //显示对应dropdown
            showSubmenu: function ($toggle) {
                var self = this;
                var $sub = self.getSub($toggle);

                self.addClassOnly($toggle, 'selected');

                // return self.addClassOnly($sub, 'show');
                return $sub.addClass('show').parent().siblings().find('.nav-menu-wrap').removeClass('show');
            },

            hideSubmenu: function ($sub) {
                var self = this;
                self.$toggles.removeClass('selected');
                self.navLocation();

                if ($sub && $sub.length > 0) {
                    return $sub.removeClass('show');
                }

                return self.$subMenus.removeClass('show');
            },

            //回到初始状态
            resetStatus: function () {
                var self = this;
                self.timer && clearTimeout(self.timer);
                self.hideSubmenu();
            },

            overHandle: function (ctx) {
                var self = this;
                var $ele = $(ctx);

                self.timer && clearTimeout(self.timer);

                //慢点粗来~~
                self.timer = setTimeout(function () {
                    self.showSubmenu($ele);
                    self.arrangement($('.docs-header #pd .wrap_pd_list .wflowBox'),$('.docs-header #pd .wrap_pd_list'));
                    self.arrangement($('.docs-header #api .wrap_pd_list .wflowBox'),$('.docs-header #api .wrap_pd_list'));
                }, self.delay);
            },

            outHandle: function (ctx) {
                var self = this;
                var $ele = $(ctx);

                self.timer && clearTimeout(self.timer);

                //慢点消失~~
                self.timer = setTimeout(function () {
                    self.hideSubmenu();
                    self.resetStatus();
                }, self.delay);
            },

            //主函数
            main: function () {
                var self = this;
                //toggle之间切换
                self.$toggles.hover(function () {
                    self.overHandle(this);
                }, function () {
                    self.outHandle(this);
                });

                //hover在subMenu上就消失不掉啦~~
                self.$subMenus.hover(function () {
                    self.timer && clearTimeout(self.timer);
                }, function () {
                    self.outHandle(this);
                });
                
            },

            //入口函数
            init: function () {
                var self = this;
                self.resetStatus();
                self.main();
            }
        };

        //go~~~
        TopMenu.init();
    })(window.jQuery);


                
    //移动端下拉菜单中收起按钮点击后，下拉菜单消失
    $('.mobile-nav-btn').on('click',function(){
        $('.nav-menu-wrap').removeClass('show');
    });
      
    // 输入框展开收起
    $('.icon__search').on('click',function(){
        $('.search-bar').addClass('icon__search_stretch');
        $('.search_goback').addClass('search_goback_show');   
    });
      
    $('.search_shutdown').on('click',function(){
        $('.search-bar').removeClass('icon__search_stretch');
        $('.search_goback').removeClass('search_goback_show');
    });

    //导航搜索
    $("#searchbtn").keyup(function(event){
        var  searchDomain = "https://www.ucloud.cn/site/search.html";
        if(event.keyCode ==13){
            var searchContent = encodeURIComponent($("#searchbtn").val());
            var uSearchUrl;
            if($.trim(url[1])==$.trim('api')){
                uSearchUrl = searchDomain+"?t=apis&k="+searchContent;  
            }else{
                uSearchUrl = searchDomain+"?t=docs&k="+searchContent;
            }
                window.open(uSearchUrl); 
                $("#searchbtn").val("");
            }
    });

    //判断是移动端还是pc端,解决fixed在ios移动端不兼容和移动端导航不同的交互
    var ua = navigator.userAgent.toLocaleLowerCase();
    var pf = navigator.platform.toLocaleLowerCase();
    var isAndroid = (/android/i).test(ua)||((/iPhone|iPod|iPad/i).test(ua) && (/linux/i).test(pf))|| (/ucweb.*linux/i.test(ua));
    var isIOS =(/iPhone|iPod|iPad/i).test(ua) && !isAndroid;
    var isWinPhone = (/Windows Phone|ZuneWP7/i).test(ua);
    var mobileType = {
        pc:!isAndroid && !isIOS && !isWinPhone,
        ios:isIOS,
        android:isAndroid,
        winPhone:isWinPhone
    };
    var windowInnerHeight = window.innerHeight;
    //移动端点击导航下拉交互
    if(!mobileType.pc){
        $('.docs-header .submenu').click(function(){
            var navhref = $(this).data("href");
            var visitURL = window.location.pathname.split('/')[1];
            var hasshow = $('.docs-header #menudropdowns  #' +navhref ).find('.nav-menu-wrap').eq(0).hasClass('show');
            if(hasshow){
                $('.docs-header #menudropdowns').find('.nav-menu-wrap').removeClass('show');
                if($.trim(visitURL) == $.trim('api')){
                    $('#topmenu>li').each(function(){
                        var name = $(this).data('href');
                        if($.trim(name) == $.trim('api')){
                            $(this).addClass('selected').siblings().removeClass('selected');
                            return false;
                        }
                    });
                }else{
                    $('#topmenu>li:first-child').addClass('selected').siblings().removeClass('selected');
                }
            }else{
                $('.docs-header #menudropdowns  #' +navhref ).find('.nav-menu-wrap').eq(0).addClass('show');
                $('.docs-header #topmenu .submenu').removeClass('selected');
                $(this).addClass('selected');
            }
        });
    };
    $(window).resize(function(){
        if(!mobileType.pc){
            if(window.innerHeight < windowInnerHeight){
                $('.docs-header').css('position','absolute');
                $(document).scrollTop(0);
            }else{
                $('.docs-header').css('position','fixed');
            };
        };
    }); 
})
