const $dropdown=$(".dropdown");const $dropdownToggle=$(".dropdown-toggle");const $dropdownMenu=$(".dropdown-menu");const showClass="show";$(window).on("load resize",function(){if(this.matchMedia("(min-width: 992px)").matches){$dropdown.hover(function(){const $this=$(this);$this.addClass(showClass);$this.find($dropdownToggle).attr("aria-expanded","true");$this.find($dropdownMenu).addClass(showClass);},function(){const $this=$(this);$this.removeClass(showClass);$this.find($dropdownToggle).attr("aria-expanded","false");$this.find($dropdownMenu).removeClass(showClass);});}else{$dropdown.off("mouseenter mouseleave");}});jQuery(document).ready(function($){if(window.jQuery().datetimepicker){$('.datetimepicker').datetimepicker({format:'YYYY-MM-DD hh:mm A',icons:{time:'fa fa-clock-o',date:'fa fa-calendar',up:'fa fa-chevron-up',down:'fa fa-chevron-down',previous:'fa fa-chevron-left',next:'fa fa-chevron-right',today:'fa fa-check',clear:'fa fa-trash',close:'fa fa-times'}});}});;