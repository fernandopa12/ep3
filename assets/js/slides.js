let current=1; const total=document.querySelectorAll('.slide').length;
const dotsContainer=document.getElementById('dots'); const counter=document.getElementById('counter');
for(let i=1;i<=total;i++){const dot=document.createElement('div');dot.className='dot'+(i===1?' active':'');dot.onclick=()=>goToSlide(i);dotsContainer.appendChild(dot);}
function goToSlide(n){const prev=document.querySelector('.slide.active');const next=document.querySelector('.slide[data-slide="'+n+'"]');if(prev)prev.classList.remove('active');if(next){next.classList.add('active');animateSlide(next);}current=n;updateNav();}
function changeSlide(dir){let n=current+dir;if(n<1)n=total;if(n>total)n=1;goToSlide(n);}
function updateNav(){document.querySelectorAll('.dot').forEach((d,i)=>d.classList.toggle('active',i+1===current));counter.textContent=current+' / '+total;}
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();changeSlide(1);}if(e.key==='ArrowLeft'){e.preventDefault();changeSlide(-1);}});
let tx=0;document.addEventListener('touchstart',e=>{tx=e.touches[0].clientX;});document.addEventListener('touchend',e=>{const d=tx-e.changedTouches[0].clientX;if(Math.abs(d)>50)changeSlide(d>0?1:-1);});
function animateSlide(slide){slide.querySelectorAll('.reveal').forEach((el,i)=>{el.style.transition='none';el.style.opacity='0';el.style.transform='translateY(12px)';el.offsetHeight;const delay=i*0.07;el.style.transition='opacity .32s ease '+delay+'s, transform .32s ease '+delay+'s';el.style.opacity='1';el.style.transform='translateY(0)';});}
try{animateSlide(document.querySelector('.slide.active'));}catch(e){console.warn(e);}
