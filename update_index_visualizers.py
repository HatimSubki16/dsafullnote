from pathlib import Path


TARGET = Path(r"C:\clone Repo\dsafullnote\index.html")


ADVANCED_CSS = r"""

/* --- ADVANCED VISUALIZER LAYOUTS --- */
.algo-tabs{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 16px}
.algo-pill{background:var(--surface2);border:1px solid var(--border);color:var(--muted);border-radius:6px;padding:7px 11px;font-size:12px;font-family:'Space Mono',monospace;cursor:pointer;transition:all .2s}
.algo-pill:hover,.algo-pill.active{border-color:var(--accent);color:var(--accent);background:rgba(0,229,197,.08)}
.viz-grid{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(260px,.9fr);gap:16px;align-items:start}
@media(max-width:760px){.viz-grid{grid-template-columns:1fr}}
.array-display{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}
.array-cell{min-width:38px;text-align:center;padding:7px 9px;border-radius:6px;background:var(--surface2);border:1px solid var(--border);color:var(--muted);font-family:'Space Mono',monospace;font-size:12px;transition:all .2s}
.array-cell.range{border-color:rgba(0,229,197,.35);color:var(--text);background:rgba(0,229,197,.05)}
.array-cell.active,.array-cell.compare{border-color:var(--accent2);color:var(--accent2);background:rgba(249,168,37,.1)}
.array-cell.min{border-color:#60a5fa;color:#60a5fa;background:rgba(96,165,250,.1)}
.array-cell.pivot{border-color:var(--accent3);color:var(--accent3);background:rgba(240,98,146,.12)}
.array-cell.sorted,.array-cell.found{border-color:#22c55e;color:#22c55e;background:rgba(34,197,94,.1)}
.array-cell.eliminated{opacity:.35}
.sort-viz-bars{height:150px}
.sort-viz-bars .sort-bar{min-width:20px;display:flex;align-items:flex-end;justify-content:center;color:#000;font-family:'Space Mono',monospace;font-size:10px;font-weight:700;padding-bottom:3px}
.sort-viz-bars .sort-bar.range{box-shadow:0 0 0 1px rgba(0,229,197,.3) inset}
.sort-viz-bars .sort-bar.min{background:#60a5fa}
.sort-viz-bars .sort-bar.pivot{background:var(--accent3)}
.step-scroll{max-height:260px;overflow:auto;border:1px solid var(--border);border-radius:8px;margin-top:12px}
.step-scroll .step-table{margin:0}
.step-comment{font-family:'Space Mono',monospace;font-size:12px;color:var(--accent2);line-height:1.55}
.step-muted{color:var(--muted)}
.viz-legend{display:flex;flex-wrap:wrap;gap:12px;margin-top:8px;font-size:11px;font-family:'Space Mono',monospace;color:var(--muted)}
.legend-dot{width:10px;height:10px;border-radius:2px;display:inline-block;margin-right:4px;vertical-align:-1px}
.node-circle.current{fill:var(--accent2);stroke:var(--accent2)}
.node-text.current{fill:#000}
.tree-note{min-height:28px;font-family:'Space Mono',monospace;font-size:12px;color:var(--accent2);margin-top:8px}
"""


CH8 = r"""
    <!-- CH 8: SORTING -->
    <div class="chapter" id="ch8">
      <div class="chapter-header">
        <span class="chapter-num">CH 08</span>
        <span class="chapter-title">Sorting Algorithms</span>
      </div>

      <div class="section" id="sort-section">
        <div class="section-title"><span class="exam-badge">⭐ EXAM</span> Sorting Complexity Summary</div>
        <table class="tbl">
          <tr><th>Algorithm</th><th>Best</th><th>Average</th><th>Worst</th><th>Space</th><th>Stable?</th><th>Inline comment</th></tr>
          <tr><td>Insertion Sort</td><td><span class="badge badge-green">O(n)</span></td><td><span class="badge badge-red">O(n²)</span></td><td><span class="badge badge-red">O(n²)</span></td><td>O(1)</td><td><span class="badge badge-green">Yes</span></td><td><span class="step-comment">// Best when already sorted; inserts each key into the sorted left side.</span></td></tr>
          <tr><td>Selection Sort</td><td><span class="badge badge-red">O(n²)</span></td><td><span class="badge badge-red">O(n²)</span></td><td><span class="badge badge-red">O(n²)</span></td><td>O(1)</td><td><span class="badge badge-red">No</span></td><td><span class="step-comment">// Always scans the remaining unsorted part to find the minimum.</span></td></tr>
          <tr><td>Bubble Sort</td><td><span class="badge badge-green">O(n)</span></td><td><span class="badge badge-red">O(n²)</span></td><td><span class="badge badge-red">O(n²)</span></td><td>O(1)</td><td><span class="badge badge-green">Yes</span></td><td><span class="step-comment">// Adjacent swaps; early stop gives O(n) when no swaps occur.</span></td></tr>
          <tr><td>Heap Sort</td><td><span class="badge badge-yellow">O(n log n)</span></td><td><span class="badge badge-yellow">O(n log n)</span></td><td><span class="badge badge-yellow">O(n log n)</span></td><td>O(1)</td><td><span class="badge badge-red">No</span></td><td><span class="step-comment">// Build a max-heap, then move the root maximum to the sorted tail.</span></td></tr>
          <tr><td>Quick Sort</td><td><span class="badge badge-yellow">O(n log n)</span></td><td><span class="badge badge-yellow">O(n log n)</span></td><td><span class="badge badge-red">O(n²)</span></td><td>O(log n)</td><td><span class="badge badge-red">No</span></td><td><span class="step-comment">// Last-element pivot; bad pivots on sorted data can degrade to O(n²).</span></td></tr>
          <tr><td>Merge Sort</td><td><span class="badge badge-yellow">O(n log n)</span></td><td><span class="badge badge-yellow">O(n log n)</span></td><td><span class="badge badge-yellow">O(n log n)</span></td><td>O(n)</td><td><span class="badge badge-green">Yes</span></td><td><span class="step-comment">// Divide, sort both halves, then merge using extra memory.</span></td></tr>
        </table>
      </div>

      <div class="section" id="all-sorting-visualizer">
        <div class="section-title"><span class="exam-badge">⭐ EXAM</span> All Sorting Visualizer</div>
        <div class="card card-accent">
          <p>This visualizer follows the PDF set: insertion, selection, bubble, heap, quick, and merge sort. Every step row includes an inline-style comment so you can read the algorithm like annotated code.</p>
        </div>

        <div class="visualizer" style="margin-top:12px">
          <div class="viz-title">Sorting Step Visualizer</div>
          <div class="algo-tabs">
            <button class="algo-pill active" data-sort-algo="insertion" onclick="setSortAlgo('insertion')">Insertion</button>
            <button class="algo-pill" data-sort-algo="selection" onclick="setSortAlgo('selection')">Selection</button>
            <button class="algo-pill" data-sort-algo="bubble" onclick="setSortAlgo('bubble')">Bubble</button>
            <button class="algo-pill" data-sort-algo="heap" onclick="setSortAlgo('heap')">Heap</button>
            <button class="algo-pill" data-sort-algo="quick" onclick="setSortAlgo('quick')">Quick</button>
            <button class="algo-pill" data-sort-algo="merge" onclick="setSortAlgo('merge')">Merge</button>
          </div>
          <div class="viz-input-row">
            <input class="viz-input" id="sort-viz-input" value="5 8 3 2 9" placeholder="Space-separated numbers"/>
            <button class="btn btn-primary" onclick="startSortViz()">Start</button>
            <button class="btn btn-secondary btn-sm" onclick="stepSortViz()">Step</button>
            <button class="btn btn-secondary btn-sm" onclick="runSortViz()">Run All</button>
            <button class="btn btn-secondary btn-sm" onclick="resetSortViz()">Reset</button>
          </div>

          <div class="viz-grid">
            <div>
              <div id="sort-viz-bars" class="sort-bars sort-viz-bars"></div>
              <div id="sort-viz-array" class="array-display"></div>
              <div class="viz-legend">
                <span><i class="legend-dot" style="background:var(--accent)"></i>normal</span>
                <span><i class="legend-dot" style="background:var(--accent2)"></i>compare/key</span>
                <span><i class="legend-dot" style="background:#60a5fa"></i>minimum</span>
                <span><i class="legend-dot" style="background:var(--accent3)"></i>pivot</span>
                <span><i class="legend-dot" style="background:#22c55e"></i>sorted/found</span>
              </div>
            </div>
            <div class="viz-panel">
              <div class="viz-panel-label">Current row comment</div>
              <div id="sort-viz-comment" class="step-comment">// Pick a sorting algorithm, then press Start.</div>
            </div>
          </div>

          <div class="step-scroll">
            <table class="step-table">
              <thead><tr><th>Row</th><th>Action</th><th>Array</th><th>Inline comment</th></tr></thead>
              <tbody id="sort-viz-steps"></tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="section">
        <div class="section-title">PDF Sorting Notes</div>
        <div class="info-grid">
          <div class="card card-accent">
            <strong>Insertion Sort</strong>
            <p>Builds the sorted list one item at a time. Mnemonic from the notes: <strong>KICK</strong> — Key stored, Iterate backwards, Compare and shift, Key placed.</p>
          </div>
          <div class="card">
            <strong>Selection Sort</strong>
            <p>Repeatedly finds the minimum in the unsorted portion and swaps it into the sorted boundary.</p>
          </div>
          <div class="card">
            <strong>Bubble Sort</strong>
            <p>Compares adjacent pairs and swaps them until no swaps are needed.</p>
          </div>
          <div class="card">
            <strong>Heap Sort</strong>
            <p>Uses a max-heap: build heap, exchange root with last unsorted item, then reheap down.</p>
          </div>
          <div class="card">
            <strong>Quick Sort</strong>
            <p>Uses divide and conquer with the last element as pivot, then recursively sorts left and right partitions.</p>
          </div>
          <div class="card card-accent">
            <strong>Merge Sort</strong>
            <p>Divide, sort left, sort right, then merge. Mnemonic from the notes: <strong>DSMC</strong> — Divide, Sort, Merge, Combined.</p>
          </div>
        </div>
      </div>
    </div><!-- /ch8 -->

"""


CH9 = r"""
    <!-- CH 9: SEARCHING -->
    <div class="chapter" id="ch9">
      <div class="chapter-header">
        <span class="chapter-num">CH 09</span>
        <span class="chapter-title">Searching</span>
      </div>

      <div class="section" id="search-section">
        <div class="section-title">Linear vs Binary Search</div>
        <table class="tbl">
          <tr><th></th><th>Linear Search</th><th>Binary Search</th><th>Inline comment</th></tr>
          <tr><td>Search type</td><td>Sequential Search</td><td>Interval Search</td><td><span class="step-comment">// Linear checks one by one; binary repeatedly halves the range.</span></td></tr>
          <tr><td>Requires sorted data?</td><td><span class="badge badge-green">No</span></td><td><span class="badge badge-red">Yes</span></td><td><span class="step-comment">// Binary search only works correctly when the input is sorted.</span></td></tr>
          <tr><td>Best case</td><td><span class="badge badge-green">O(1)</span></td><td><span class="badge badge-green">O(1)</span></td><td><span class="step-comment">// Target is found immediately.</span></td></tr>
          <tr><td>Average</td><td><span class="badge badge-yellow">O(n)</span></td><td><span class="badge badge-green">O(log n)</span></td><td><span class="step-comment">// Binary wins by discarding half the array each row.</span></td></tr>
          <tr><td>Worst case</td><td><span class="badge badge-red">O(n)</span></td><td><span class="badge badge-green">O(log n)</span></td><td><span class="step-comment">// Linear may inspect all items; binary stops after range crosses.</span></td></tr>
        </table>
      </div>

      <div class="section" id="search-visualizer-section">
        <div class="section-title"><span class="exam-badge">⭐ EXAM</span> Search Visualizer</div>
        <div class="card card-accent">
          <p>The PDF details sequential/linear search and binary search. Use the row comments to see exactly why the next index or range is chosen.</p>
        </div>

        <div class="visualizer" style="margin-top:12px">
          <div class="viz-title">Search Step Visualizer</div>
          <div class="algo-tabs">
            <button class="algo-pill active" data-search-algo="linear" onclick="setSearchAlgo('linear')">Linear Search</button>
            <button class="algo-pill" data-search-algo="binary" onclick="setSearchAlgo('binary')">Binary Search</button>
          </div>
          <div class="viz-input-row">
            <input class="viz-input" id="search-input" value="4 7 8 10 14 21 22 36 62 77 81 91" placeholder="Numbers"/>
            <input class="viz-input" id="search-key" value="62" placeholder="Target" style="flex:0;width:92px"/>
            <button class="btn btn-primary" onclick="startSearchViz()">Start</button>
            <button class="btn btn-secondary btn-sm" onclick="stepSearchViz()">Step</button>
            <button class="btn btn-secondary btn-sm" onclick="runSearchViz()">Run All</button>
            <button class="btn btn-secondary btn-sm" onclick="resetSearchViz()">Reset</button>
          </div>
          <div id="search-display" class="array-display"></div>
          <div id="search-comment" class="step-comment">// Choose linear or binary search, then press Start.</div>
          <div class="viz-legend">
            <span><i class="legend-dot" style="background:var(--accent)"></i>active range</span>
            <span><i class="legend-dot" style="background:var(--accent2)"></i>current / mid</span>
            <span><i class="legend-dot" style="background:#22c55e"></i>found</span>
            <span><i class="legend-dot" style="background:var(--border)"></i>eliminated</span>
          </div>
          <div class="step-scroll">
            <table class="step-table">
              <thead><tr><th>Row</th><th>Low</th><th>High</th><th>Mid/Index</th><th>Decision</th><th>Inline comment</th></tr></thead>
              <tbody id="search-steps"></tbody>
            </table>
          </div>
        </div>
      </div>
    </div><!-- /ch9 -->

"""


TREE_VISUALIZERS = r"""
        <!-- Enhanced tree visualizers -->
        <div class="visualizer" style="margin-top:16px">
          <div class="viz-title">Interactive Tree Traversal</div>
          <div style="margin-bottom:12px;display:flex;gap:8px;flex-wrap:wrap">
            <button class="btn btn-primary btn-sm" onclick="runTraversal('preorder')">Preorder (VLR)</button>
            <button class="btn btn-secondary btn-sm" onclick="runTraversal('inorder')">Inorder (LVR)</button>
            <button class="btn btn-secondary btn-sm" onclick="runTraversal('postorder')">Postorder (LRV)</button>
            <button class="btn btn-secondary btn-sm" onclick="runTraversal('bfs')">BFS Level Order</button>
            <button class="btn btn-secondary btn-sm" onclick="resetTreeViz()">Reset</button>
          </div>
          <div class="viz-grid">
            <div>
              <svg id="treeSvg" class="tree-svg" viewBox="0 0 500 220" width="100%" height="220"></svg>
              <div id="traversal-output" class="tree-note"></div>
            </div>
            <div class="step-scroll" style="max-height:220px;margin-top:0">
              <table class="step-table">
                <thead><tr><th>Row</th><th>Visit</th><th>Output</th><th>Inline comment</th></tr></thead>
                <tbody id="traversal-steps-body"></tbody>
              </table>
            </div>
          </div>
        </div>

        <div class="visualizer" style="margin-top:16px">
          <div class="viz-title">BST Insert &amp; Search Visualizer</div>
          <div class="viz-input-row">
            <input class="viz-input" id="bst-input" value="50 30 70 20 40 60 80" placeholder="BST values"/>
            <input class="viz-input" id="bst-key" value="60" placeholder="Key" style="flex:0;width:90px"/>
            <button class="btn btn-primary" onclick="startBstBuild()">Build BST</button>
            <button class="btn btn-secondary btn-sm" onclick="startBstSearch()">Search Key</button>
            <button class="btn btn-secondary btn-sm" onclick="insertBstKey()">Insert Key</button>
            <button class="btn btn-secondary btn-sm" onclick="resetBstViz()">Reset</button>
          </div>
          <div class="viz-grid">
            <div>
              <svg id="bstSvg" class="tree-svg" viewBox="0 0 560 260" width="100%" height="260"></svg>
              <div id="bst-note" class="tree-note">// BST rule: left child key &lt; parent key &lt; right child key.</div>
            </div>
            <div class="step-scroll" style="max-height:260px;margin-top:0">
              <table class="step-table">
                <thead><tr><th>Row</th><th>Node</th><th>Decision</th><th>Inline comment</th></tr></thead>
                <tbody id="bst-steps-body"></tbody>
              </table>
            </div>
          </div>
        </div>

        <div class="visualizer" style="margin-top:16px">
          <div class="viz-title">Expression Tree → Postfix Visualizer</div>
          <div class="viz-input-row">
            <button class="btn btn-primary" onclick="runExpressionPostfix()">Run Postorder</button>
            <button class="btn btn-secondary btn-sm" onclick="resetExpressionViz()">Reset</button>
          </div>
          <div class="viz-grid">
            <div>
              <svg id="exprSvg" class="tree-svg" viewBox="0 0 360 210" width="100%" height="210"></svg>
              <div id="expr-output" class="tree-note">// Postorder on A * (B + C) produces postfix: A B C + *</div>
            </div>
            <div class="step-scroll" style="max-height:220px;margin-top:0">
              <table class="step-table">
                <thead><tr><th>Row</th><th>Visit</th><th>Output</th><th>Inline comment</th></tr></thead>
                <tbody id="expr-steps-body"></tbody>
              </table>
            </div>
          </div>
        </div>
"""


ADVANCED_JS = r"""

// -------------------------------------------------------------
// ADVANCED VISUALIZERS ADDED FROM THE PDF NOTES
// -------------------------------------------------------------
function vizEscape(value){
  return String(value).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
}
function parseVizNumbers(id){
  const el = document.getElementById(id);
  if(!el) return [];
  return el.value.trim().split(/\s+/).map(Number).filter(v => Number.isFinite(v)).slice(0, 14);
}
function setAlgoButtonActive(selector, attr, value){
  document.querySelectorAll(selector).forEach(btn => btn.classList.toggle('active', btn.getAttribute(attr) === value));
}
function rangeIndices(start, endInclusive){
  const out = [];
  for(let i=start;i<=endInclusive;i++) out.push(i);
  return out;
}

// SORTING VISUALIZER
var sortVizState = {algo:'insertion', steps:[], index:-1, timer:null};
function makeSortStep(arr, action, comment, meta={}){
  return Object.assign({arr:[...arr], action, comment, compare:[], sorted:[], range:[], min:[], pivot:null}, meta);
}
function setSortAlgo(algo){
  sortVizState.algo = algo;
  setAlgoButtonActive('[data-sort-algo]', 'data-sort-algo', algo);
  resetSortViz();
}
function buildSortVizSteps(algo, input){
  if(algo==='selection') return buildSelectionSteps(input);
  if(algo==='bubble') return buildBubbleSteps(input);
  if(algo==='heap') return buildHeapSteps(input);
  if(algo==='quick') return buildQuickSteps(input);
  if(algo==='merge') return buildMergeSteps(input);
  return buildInsertionSteps(input);
}
function buildInsertionSteps(input){
  const a=[...input], steps=[makeSortStep(a,'Start insertion sort','// Start: arr[0] is treated as the first sorted region.',{sorted:a.length? [0]:[]})];
  for(let i=1;i<a.length;i++){
    const key=a[i]; let j=i-1;
    steps.push(makeSortStep(a,`Pick key ${key} at index ${i}`,`// key=${key}; compare backward inside arr[0..${i-1}] and open a gap.`,{compare:[i],sorted:rangeIndices(0,i-1)}));
    while(j>=0 && a[j]>key){
      a[j+1]=a[j];
      steps.push(makeSortStep(a,`Shift ${a[j]} right`, `// arr[${j}]=${a[j]} is greater than key=${key}, so move it to index ${j+1}.`,{compare:[j,j+1],sorted:rangeIndices(0,i)}));
      j--;
    }
    a[j+1]=key;
    steps.push(makeSortStep(a,`Insert key ${key}`,`// Place key=${key} into the gap at index ${j+1}; sorted region grows to arr[0..${i}].`,{compare:[j+1],sorted:rangeIndices(0,i)}));
  }
  steps.push(makeSortStep(a,'Done','// All keys have been inserted into the sorted left side.',{sorted:rangeIndices(0,a.length-1)}));
  return steps;
}
function buildSelectionSteps(input){
  const a=[...input], steps=[makeSortStep(a,'Start selection sort','// Start: repeatedly select the minimum from the unsorted suffix.')];
  for(let i=0;i<a.length-1;i++){
    let min=i;
    steps.push(makeSortStep(a,`Set index ${i} as temporary minimum`,`// Sorted boundary is index ${i}; search arr[${i}..${a.length-1}] for the minimum.`,{min:[min],range:rangeIndices(i,a.length-1),sorted:rangeIndices(0,i-1)}));
    for(let j=i+1;j<a.length;j++){
      steps.push(makeSortStep(a,`Compare ${a[j]} with current min ${a[min]}`,`// If arr[${j}] < arr[${min}], update the minimum pointer.`,{compare:[j],min:[min],range:rangeIndices(i,a.length-1),sorted:rangeIndices(0,i-1)}));
      if(a[j]<a[min]){
        min=j;
        steps.push(makeSortStep(a,`New minimum is ${a[min]}`,`// arr[${j}] is the smallest seen so far in the unsorted region.`,{min:[min],range:rangeIndices(i,a.length-1),sorted:rangeIndices(0,i-1)}));
      }
    }
    if(min!==i){
      [a[i],a[min]]=[a[min],a[i]];
      steps.push(makeSortStep(a,`Swap minimum into index ${i}`,`// Move the minimum to the sorted boundary; selection sort does one final swap per pass.`,{compare:[i,min],sorted:rangeIndices(0,i)}));
    } else {
      steps.push(makeSortStep(a,`Index ${i} already correct`,`// Minimum is already at the boundary; no swap needed for this pass.`,{sorted:rangeIndices(0,i)}));
    }
  }
  steps.push(makeSortStep(a,'Done','// Every boundary position has received the minimum from its unsorted suffix.',{sorted:rangeIndices(0,a.length-1)}));
  return steps;
}
function buildBubbleSteps(input){
  const a=[...input], steps=[makeSortStep(a,'Start bubble sort','// Start: compare adjacent pairs and bubble the largest value to the end.')];
  for(let pass=0;pass<a.length-1;pass++){
    let swapped=false;
    for(let i=0;i<a.length-pass-1;i++){
      steps.push(makeSortStep(a,`Compare indexes ${i} and ${i+1}`,`// Adjacent check: if ${a[i]} > ${a[i+1]}, swap them.`,{compare:[i,i+1],sorted:rangeIndices(a.length-pass,a.length-1)}));
      if(a[i]>a[i+1]){
        [a[i],a[i+1]]=[a[i+1],a[i]];
        swapped=true;
        steps.push(makeSortStep(a,`Swap ${a[i]} and ${a[i+1]}`,`// Wrong order fixed; the larger value moves one step toward the sorted tail.`,{compare:[i,i+1],sorted:rangeIndices(a.length-pass,a.length-1)}));
      }
    }
    steps.push(makeSortStep(a,`Pass ${pass+1} complete`,`// The largest remaining value is now locked at index ${a.length-pass-1}.`,{sorted:rangeIndices(a.length-pass-1,a.length-1)}));
    if(!swapped){
      steps.push(makeSortStep(a,'Early stop','// No swaps happened in this pass, so the array is already sorted: best case O(n).',{sorted:rangeIndices(0,a.length-1)}));
      break;
    }
  }
  steps.push(makeSortStep(a,'Done','// Bubble sort completed after adjacent comparisons.',{sorted:rangeIndices(0,a.length-1)}));
  return steps;
}
function buildHeapSteps(input){
  const a=[...input], steps=[makeSortStep(a,'Start heap sort','// Start: build a max-heap, then move the max root to the sorted tail.')];
  function heapify(size, root){
    while(true){
      let largest=root, left=2*root+1, right=2*root+2;
      steps.push(makeSortStep(a,`Heapify root index ${root}`,`// Children use array formulas: left=2i+1 (${left}), right=2i+2 (${right}).`,{compare:[root,left,right].filter(i=>i<size),range:rangeIndices(0,size-1),sorted:rangeIndices(size,a.length-1)}));
      if(left<size && a[left]>a[largest]) largest=left;
      if(right<size && a[right]>a[largest]) largest=right;
      if(largest!==root){
        [a[root],a[largest]]=[a[largest],a[root]];
        steps.push(makeSortStep(a,`Swap parent with larger child`,`// Max-heap rule restored locally: parent must be greater than or equal to children.`,{compare:[root,largest],range:rangeIndices(0,size-1),sorted:rangeIndices(size,a.length-1)}));
        root=largest;
      } else {
        steps.push(makeSortStep(a,`Subtree already satisfies heap rule`,`// No child is larger than the parent, so this heapify path stops.`,{compare:[root],range:rangeIndices(0,size-1),sorted:rangeIndices(size,a.length-1)}));
        break;
      }
    }
  }
  for(let i=Math.floor(a.length/2)-1;i>=0;i--) heapify(a.length,i);
  steps.push(makeSortStep(a,'Max-heap built','// Root now stores the maximum value in the unsorted heap.',{range:rangeIndices(0,a.length-1)}));
  for(let end=a.length-1;end>0;end--){
    [a[0],a[end]]=[a[end],a[0]];
    steps.push(makeSortStep(a,`Move max to index ${end}`,`// Swap root maximum into the sorted tail; heap size shrinks by one.`,{compare:[0,end],sorted:rangeIndices(end,a.length-1),range:rangeIndices(0,end-1)}));
    heapify(end,0);
  }
  steps.push(makeSortStep(a,'Done','// Heap sort is complete; sorted tail expanded across the whole array.',{sorted:rangeIndices(0,a.length-1)}));
  return steps;
}
function buildQuickSteps(input){
  const a=[...input], steps=[makeSortStep(a,'Start quick sort','// Start: choose the last item as pivot, partition, then recurse.')];
  function partition(low, high){
    const pivot=a[high]; let i=low-1;
    steps.push(makeSortStep(a,`Pivot ${pivot} at index ${high}`,`// Last-element pivot from the notes; values < pivot move left.`,{pivot:high,range:rangeIndices(low,high)}));
    for(let j=low;j<high;j++){
      steps.push(makeSortStep(a,`Compare ${a[j]} with pivot ${pivot}`,`// If arr[${j}] < pivot, advance i and swap into the left partition.`,{compare:[j],pivot:high,range:rangeIndices(low,high)}));
      if(a[j]<pivot){
        i++;
        [a[i],a[j]]=[a[j],a[i]];
        steps.push(makeSortStep(a,`Place ${a[i]} in left partition`,`// arr[${i}] is now confirmed less than pivot; boundary i moves right.`,{compare:[i,j],pivot:high,range:rangeIndices(low,high)}));
      }
    }
    [a[i+1],a[high]]=[a[high],a[i+1]];
    steps.push(makeSortStep(a,`Pivot lands at index ${i+1}`,`// Pivot is now between smaller-left and greater-or-equal-right partitions.`,{pivot:i+1,range:rangeIndices(low,high)}));
    return i+1;
  }
  function quick(low, high){
    if(low<high){
      steps.push(makeSortStep(a,`Partition range ${low}..${high}`,`// Recurse only inside this active partition.`,{range:rangeIndices(low,high)}));
      const p=partition(low,high);
      quick(low,p-1);
      quick(p+1,high);
    } else if(low===high){
      steps.push(makeSortStep(a,`Single item at index ${low}`,`// Base case: one element is already sorted.`,{sorted:[low]}));
    }
  }
  quick(0,a.length-1);
  steps.push(makeSortStep(a,'Done','// All partitions reached base case; quick sort is complete.',{sorted:rangeIndices(0,a.length-1)}));
  return steps;
}
function buildMergeSteps(input){
  const a=[...input], steps=[makeSortStep(a,'Start merge sort','// Start: divide into halves, sort both halves, then merge.')];
  function mergeSort(left,right){
    if(left>=right){
      steps.push(makeSortStep(a,`Base case index ${left}`,`// One element is already sorted; return to merge step.`,{range:[left]}));
      return;
    }
    const mid=Math.floor((left+right)/2);
    steps.push(makeSortStep(a,`Split ${left}..${right}`,`// mid=${mid}; sort left half ${left}..${mid}, then right half ${mid+1}..${right}.`,{range:rangeIndices(left,right)}));
    mergeSort(left,mid);
    mergeSort(mid+1,right);
    const L=a.slice(left,mid+1), R=a.slice(mid+1,right+1);
    let i=0,j=0,k=left;
    steps.push(makeSortStep(a,`Merge ${left}..${mid} and ${mid+1}..${right}`,`// Compare the front of each sorted half and copy the smaller value back.`,{range:rangeIndices(left,right)}));
    while(i<L.length && j<R.length){
      if(L[i]<=R[j]){
        a[k]=L[i];
        steps.push(makeSortStep(a,`Copy ${L[i]} from left half`,`// ${L[i]} <= ${R[j]}, so left value fills arr[${k}].`,{compare:[k],range:rangeIndices(left,right)}));
        i++;
      } else {
        a[k]=R[j];
        steps.push(makeSortStep(a,`Copy ${R[j]} from right half`,`// ${R[j]} < ${L[i]}, so right value fills arr[${k}].`,{compare:[k],range:rangeIndices(left,right)}));
        j++;
      }
      k++;
    }
    while(i<L.length){
      a[k]=L[i];
      steps.push(makeSortStep(a,`Copy remaining ${L[i]}`,`// Left half has leftover value; append it at arr[${k}].`,{compare:[k],range:rangeIndices(left,right)}));
      i++; k++;
    }
    while(j<R.length){
      a[k]=R[j];
      steps.push(makeSortStep(a,`Copy remaining ${R[j]}`,`// Right half has leftover value; append it at arr[${k}].`,{compare:[k],range:rangeIndices(left,right)}));
      j++; k++;
    }
    steps.push(makeSortStep(a,`Merged range ${left}..${right}`,`// This range is now sorted before returning upward.`,{sorted:rangeIndices(left,right)}));
  }
  if(a.length) mergeSort(0,a.length-1);
  steps.push(makeSortStep(a,'Done','// Final merge produced one fully sorted array.',{sorted:rangeIndices(0,a.length-1)}));
  return steps;
}
function classForSortIndex(step,i){
  const cls=[];
  if(step.range && step.range.includes(i)) cls.push('range');
  if(step.sorted && step.sorted.includes(i)) cls.push('sorted');
  if(step.compare && step.compare.includes(i)) cls.push('compare');
  if(step.min && step.min.includes(i)) cls.push('min');
  if(step.pivot===i) cls.push('pivot');
  return cls.join(' ');
}
function renderSortViz(){
  const bars=document.getElementById('sort-viz-bars'), cells=document.getElementById('sort-viz-array'), body=document.getElementById('sort-viz-steps'), comment=document.getElementById('sort-viz-comment');
  if(!bars || !cells || !body || !comment) return;
  const step=sortVizState.steps[sortVizState.index];
  if(!step){
    bars.innerHTML=''; cells.innerHTML=''; body.innerHTML=''; comment.textContent='// Pick a sorting algorithm, then press Start.'; return;
  }
  const max=Math.max(...step.arr.map(v=>Math.abs(v)),1);
  bars.innerHTML=step.arr.map((v,i)=>`<div class="sort-bar ${classForSortIndex(step,i)}" style="height:${Math.max(12,Math.abs(v)/max*130)}px" title="index ${i}: ${v}">${vizEscape(v)}</div>`).join('');
  cells.innerHTML=step.arr.map((v,i)=>`<div class="array-cell ${classForSortIndex(step,i)}">${vizEscape(v)}<div class="step-muted">${i}</div></div>`).join('');
  comment.textContent=step.comment;
  body.innerHTML=sortVizState.steps.slice(0,sortVizState.index+1).map((s,i)=>`<tr class="${i===sortVizState.index?'current-step':''}"><td>${i+1}</td><td>${vizEscape(s.action)}</td><td>${vizEscape(s.arr.join(' '))}</td><td class="step-comment">${vizEscape(s.comment)}</td></tr>`).join('');
  body.lastElementChild?.scrollIntoView({block:'nearest'});
}
function startSortViz(){
  clearTimeout(sortVizState.timer);
  const values=parseVizNumbers('sort-viz-input');
  if(!values.length) return;
  sortVizState.steps=buildSortVizSteps(sortVizState.algo, values);
  sortVizState.index=0;
  renderSortViz();
}
function stepSortViz(){
  clearTimeout(sortVizState.timer);
  if(!sortVizState.steps.length){ startSortViz(); return; }
  if(sortVizState.index<sortVizState.steps.length-1) sortVizState.index++;
  renderSortViz();
}
function runSortViz(){
  if(!sortVizState.steps.length) startSortViz();
  clearTimeout(sortVizState.timer);
  const tick=()=>{
    if(sortVizState.index<sortVizState.steps.length-1){
      sortVizState.index++;
      renderSortViz();
      sortVizState.timer=setTimeout(tick,420);
    }
  };
  tick();
}
function resetSortViz(){
  clearTimeout(sortVizState.timer);
  sortVizState.steps=[]; sortVizState.index=-1;
  renderSortViz();
}

// ENHANCED TREE TRAVERSAL
const treeVizData = {
  val:'A', id:0,
  left:{val:'B', id:1, left:{val:'D',id:3,left:null,right:null}, right:{val:'E',id:4,left:null,right:null}},
  right:{val:'C', id:2, left:{val:'F',id:5,left:null,right:null}, right:{val:'G',id:6,left:null,right:null}}
};
const treeVizPositions = {0:[250,30],1:[125,90],2:[375,90],3:[65,155],4:[185,155],5:[315,155],6:[435,155]};
const treeVizEdges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]];
var traversalTimer=null;
function findTreeVizNode(tree,id){ if(!tree)return null; if(tree.id===id)return tree; return findTreeVizNode(tree.left,id)||findTreeVizNode(tree.right,id); }
function drawTree(visitedSet=new Set(), currentId=null){
  const svg=document.getElementById('treeSvg');
  if(!svg) return;
  svg.innerHTML='';
  treeVizEdges.forEach(([a,b])=>{
    const [x1,y1]=treeVizPositions[a], [x2,y2]=treeVizPositions[b];
    svg.innerHTML+=`<line x1="${x1}" y1="${y1+18}" x2="${x2}" y2="${y2-18}" class="tree-edge"/>`;
  });
  Object.entries(treeVizPositions).forEach(([id,[x,y]])=>{
    const node=findTreeVizNode(treeVizData,parseInt(id));
    const visited=visitedSet.has(parseInt(id)), current=parseInt(id)===currentId;
    svg.innerHTML+=`<circle cx="${x}" cy="${y}" r="18" class="node-circle${visited?' visited':''}${current?' current':''}"/><text x="${x}" y="${y}" class="node-text${visited?' visited':''}${current?' current':''}">${node.val}</text>`;
  });
}
function getOrder(type){
  const result=[];
  function preorder(n){if(!n)return;result.push(n.id);preorder(n.left);preorder(n.right);}
  function inorder(n){if(!n)return;inorder(n.left);result.push(n.id);inorder(n.right);}
  function postorder(n){if(!n)return;postorder(n.left);postorder(n.right);result.push(n.id);}
  function bfs(root){const q=[root];while(q.length){const n=q.shift();if(!n)continue;result.push(n.id);q.push(n.left,n.right);}}
  if(type==='preorder')preorder(treeVizData);
  else if(type==='inorder')inorder(treeVizData);
  else if(type==='postorder')postorder(treeVizData);
  else bfs(treeVizData);
  return result;
}
function traversalComment(type, label, output){
  if(type==='preorder') return `// Visit ${label} before its children because preorder is VLR: Root, Left, Right.`;
  if(type==='inorder') return `// Visit ${label} between left and right because inorder is LVR: Left, Root, Right.`;
  if(type==='postorder') return `// Visit ${label} after its children because postorder is LRV and creates postfix order.`;
  return `// Visit ${label} from the queue; BFS processes the tree level by level.`;
}
function runTraversal(type){
  clearTimeout(traversalTimer);
  const order=getOrder(type), visited=new Set(), rows=[], labels={preorder:'Preorder (VLR)',inorder:'Inorder (LVR)',postorder:'Postorder (LRV)',bfs:'BFS Level Order'};
  const body=document.getElementById('traversal-steps-body'), out=document.getElementById('traversal-output');
  function tick(i){
    if(i>=order.length) return;
    const id=order[i], node=findTreeVizNode(treeVizData,id);
    visited.add(id);
    const output=order.slice(0,i+1).map(nid=>findTreeVizNode(treeVizData,nid).val).join(' → ');
    rows.push({visit:node.val, output, comment:traversalComment(type,node.val,output)});
    drawTree(visited,id);
    if(out) out.textContent=`${labels[type]}: ${output}`;
    if(body) body.innerHTML=rows.map((r,idx)=>`<tr class="${idx===rows.length-1?'current-step':''}"><td>${idx+1}</td><td>${r.visit}</td><td>${r.output}</td><td class="step-comment">${vizEscape(r.comment)}</td></tr>`).join('');
    body?.lastElementChild?.scrollIntoView({block:'nearest'});
    traversalTimer=setTimeout(()=>tick(i+1),520);
  }
  if(body) body.innerHTML='';
  tick(0);
}
function resetTreeViz(){
  clearTimeout(traversalTimer);
  drawTree();
  const out=document.getElementById('traversal-output'), body=document.getElementById('traversal-steps-body');
  if(out) out.textContent='// Choose a traversal. Each output row will explain why that node is visited.';
  if(body) body.innerHTML='';
}

// BST VISUALIZER
var bstRoot=null, bstCurrentKey=null;
function makeBstNode(value){ return {value,left:null,right:null}; }
function bstValuesFromInput(){ return [...new Set(parseVizNumbers('bst-input'))]; }
function bstInsertWithSteps(value, steps){
  if(!bstRoot){
    bstRoot=makeBstNode(value);
    steps.push({node:'root',decision:`Create ${value}`,comment:`// Tree is empty, so ${value} becomes the root.`});
    return;
  }
  let cur=bstRoot;
  while(cur){
    if(value<cur.value){
      steps.push({node:cur.value,decision:`${value} < ${cur.value}: go left`,comment:`// BST rule sends smaller keys to the left child.`});
      if(!cur.left){cur.left=makeBstNode(value);steps.push({node:cur.value,decision:`Insert ${value} as left child`,comment:`// Empty left link found; attach the new node here.`});return;}
      cur=cur.left;
    } else if(value>cur.value){
      steps.push({node:cur.value,decision:`${value} > ${cur.value}: go right`,comment:`// BST rule sends larger keys to the right child.`});
      if(!cur.right){cur.right=makeBstNode(value);steps.push({node:cur.value,decision:`Insert ${value} as right child`,comment:`// Empty right link found; attach the new node here.`});return;}
      cur=cur.right;
    } else {
      steps.push({node:cur.value,decision:`${value} already exists`,comment:`// Duplicate key ignored so the visualization stays clear.`});
      return;
    }
  }
}
function renderBstTree(currentValue=null){
  const svg=document.getElementById('bstSvg');
  if(!svg) return;
  svg.innerHTML='';
  if(!bstRoot){ svg.innerHTML='<text x="24" y="42" fill="var(--muted)" font-size="13">Build the BST to visualize it.</text>'; return; }
  const nodes=[], edges=[];
  let nextX=42, maxDepth=0;
  function assign(n, depth){
    if(!n) return;
    assign(n.left, depth+1);
    n.x=nextX; n.y=34+depth*64; nextX+=68; maxDepth=Math.max(maxDepth,depth);
    nodes.push(n);
    if(n.left) edges.push([n,n.left]);
    if(n.right) edges.push([n,n.right]);
    assign(n.right, depth+1);
  }
  assign(bstRoot,0);
  const width=Math.max(560,nextX+42), height=Math.max(250,80+maxDepth*64);
  svg.setAttribute('viewBox',`0 0 ${width} ${height}`);
  edges.forEach(([a,b])=>{ svg.innerHTML+=`<line x1="${a.x}" y1="${a.y+18}" x2="${b.x}" y2="${b.y-18}" class="tree-edge"/>`; });
  nodes.forEach(n=>{
    const current=n.value===currentValue;
    svg.innerHTML+=`<circle cx="${n.x}" cy="${n.y}" r="18" class="node-circle${current?' current':''}"/><text x="${n.x}" y="${n.y}" class="node-text${current?' current':''}">${n.value}</text>`;
  });
}
function renderBstRows(steps, currentIndex=steps.length-1){
  const body=document.getElementById('bst-steps-body'), note=document.getElementById('bst-note');
  if(body) body.innerHTML=steps.map((s,i)=>`<tr class="${i===currentIndex?'current-step':''}"><td>${i+1}</td><td>${vizEscape(s.node)}</td><td>${vizEscape(s.decision)}</td><td class="step-comment">${vizEscape(s.comment)}</td></tr>`).join('');
  if(note && steps[currentIndex]) note.textContent=steps[currentIndex].comment;
}
function startBstBuild(){
  const values=bstValuesFromInput(), steps=[];
  bstRoot=null; bstCurrentKey=null;
  values.forEach(v=>bstInsertWithSteps(v,steps));
  renderBstTree();
  renderBstRows(steps);
}
function startBstSearch(){
  if(!bstRoot) startBstBuild();
  const key=parseInt(document.getElementById('bst-key')?.value,10);
  if(!Number.isFinite(key)) return;
  const steps=[]; let cur=bstRoot;
  while(cur){
    bstCurrentKey=cur.value;
    if(key===cur.value){ steps.push({node:cur.value,decision:`Found ${key}`,comment:`// key == node, so the BST search succeeds here.`}); break; }
    if(key<cur.value){ steps.push({node:cur.value,decision:`${key} < ${cur.value}: search left`,comment:`// Smaller than current node, discard the right subtree.`}); cur=cur.left; }
    else { steps.push({node:cur.value,decision:`${key} > ${cur.value}: search right`,comment:`// Larger than current node, discard the left subtree.`}); cur=cur.right; }
  }
  if(!cur) steps.push({node:'NULL',decision:`${key} not found`,comment:`// Reached a null child, so the key is not in this BST.`});
  let i=0;
  function tick(){
    const step=steps[i];
    const current=Number.isFinite(Number(step.node))?Number(step.node):null;
    renderBstTree(current);
    renderBstRows(steps.slice(0,i+1),i);
    if(i<steps.length-1){ i++; setTimeout(tick,520); }
  }
  tick();
}
function insertBstKey(){
  if(!bstRoot) startBstBuild();
  const key=parseInt(document.getElementById('bst-key')?.value,10);
  if(!Number.isFinite(key)) return;
  const steps=[];
  bstInsertWithSteps(key,steps);
  const input=document.getElementById('bst-input');
  if(input && !parseVizNumbers('bst-input').includes(key)) input.value = (input.value.trim() + ' ' + key).trim();
  renderBstTree(key);
  renderBstRows(steps);
}
function resetBstViz(){
  bstRoot=null; bstCurrentKey=null;
  renderBstTree();
  const body=document.getElementById('bst-steps-body'), note=document.getElementById('bst-note');
  if(body) body.innerHTML='';
  if(note) note.textContent='// BST rule: left child key < parent key < right child key.';
}

// EXPRESSION TREE VISUALIZER
const exprNodes = {
  mul:{id:'mul',val:'*',x:180,y:28},
  a:{id:'a',val:'A',x:95,y:92},
  plus:{id:'plus',val:'+',x:265,y:92},
  b:{id:'b',val:'B',x:225,y:156},
  c:{id:'c',val:'C',x:305,y:156}
};
const exprEdges=[['mul','a'],['mul','plus'],['plus','b'],['plus','c']];
var exprTimer=null;
function drawExpressionTree(visited=new Set(), current=null){
  const svg=document.getElementById('exprSvg');
  if(!svg) return;
  svg.innerHTML='';
  exprEdges.forEach(([p,ch])=>{
    const a=exprNodes[p], b=exprNodes[ch];
    svg.innerHTML+=`<line x1="${a.x}" y1="${a.y+18}" x2="${b.x}" y2="${b.y-18}" class="tree-edge"/>`;
  });
  Object.values(exprNodes).forEach(n=>{
    const v=visited.has(n.id), c=current===n.id;
    svg.innerHTML+=`<circle cx="${n.x}" cy="${n.y}" r="18" class="node-circle${v?' visited':''}${c?' current':''}"/><text x="${n.x}" y="${n.y}" class="node-text${v?' visited':''}${c?' current':''}">${n.val}</text>`;
  });
}
function runExpressionPostfix(){
  clearTimeout(exprTimer);
  const order=['a','b','c','plus','mul'], visited=new Set(), rows=[], body=document.getElementById('expr-steps-body'), out=document.getElementById('expr-output');
  function tick(i){
    if(i>=order.length) return;
    const id=order[i], node=exprNodes[id];
    visited.add(id);
    const output=order.slice(0,i+1).map(k=>exprNodes[k].val).join(' ');
    const comment = id==='plus' || id==='mul'
      ? `// Operator ${node.val} is output after its operands because postorder is Left, Right, Root.`
      : `// Operand ${node.val} is a leaf, so output it immediately when reached.`;
    rows.push({visit:node.val, output, comment});
    drawExpressionTree(visited,id);
    if(out) out.textContent=`Postfix output: ${output}`;
    if(body) body.innerHTML=rows.map((r,idx)=>`<tr class="${idx===rows.length-1?'current-step':''}"><td>${idx+1}</td><td>${r.visit}</td><td>${r.output}</td><td class="step-comment">${vizEscape(r.comment)}</td></tr>`).join('');
    body?.lastElementChild?.scrollIntoView({block:'nearest'});
    exprTimer=setTimeout(()=>tick(i+1),550);
  }
  if(body) body.innerHTML='';
  tick(0);
}
function resetExpressionViz(){
  clearTimeout(exprTimer);
  drawExpressionTree();
  const body=document.getElementById('expr-steps-body'), out=document.getElementById('expr-output');
  if(body) body.innerHTML='';
  if(out) out.textContent='// Postorder on A * (B + C) produces postfix: A B C + *';
}

// SEARCH VISUALIZER
var searchVizState={algo:'linear',steps:[],index:-1,timer:null};
function setSearchAlgo(algo){
  searchVizState.algo=algo;
  setAlgoButtonActive('[data-search-algo]', 'data-search-algo', algo);
  resetSearchViz();
}
function buildSearchSteps(algo, arr, key){
  if(algo==='binary') return buildBinarySearchSteps(arr,key);
  return buildLinearSearchSteps(arr,key);
}
function buildLinearSearchSteps(arr,key){
  const steps=[];
  for(let i=0;i<arr.length;i++){
    if(arr[i]===key){
      steps.push({arr,key,low:0,high:arr.length-1,index:i,found:i,decision:`arr[${i}] == ${key}: FOUND`,comment:`// Linear search stops as soon as index ${i} matches the target.`});
      return steps;
    }
    steps.push({arr,key,low:0,high:arr.length-1,index:i,scanned:rangeIndices(0,i),decision:`arr[${i}] = ${arr[i]}: keep going`,comment:`// Not a match, so sequential search moves to the next row/index.`});
  }
  steps.push({arr,key,low:0,high:arr.length-1,index:-1,scanned:rangeIndices(0,arr.length-1),decision:`${key} not found`,comment:`// End of array reached without a match, so return -1.`});
  return steps;
}
function buildBinarySearchSteps(arr,key){
  const sorted=arr.every((v,i)=>i===0 || arr[i-1]<=v);
  if(!sorted) return [{arr,key,low:0,high:arr.length-1,index:-1,error:true,decision:'Input is not sorted',comment:'// Binary search requires sorted input; sort the numbers first.'}];
  const steps=[]; let low=0, high=arr.length-1;
  while(low<=high){
    const mid=Math.floor((low+high)/2);
    if(arr[mid]===key){
      steps.push({arr,key,low,high,index:mid,found:mid,decision:`arr[${mid}] == ${key}: FOUND`,comment:`// Middle value matches the target, so return index ${mid}.`});
      return steps;
    }
    if(key<arr[mid]){
      steps.push({arr,key,low,high,index:mid,nextLow:low,nextHigh:mid-1,decision:`${key} < ${arr[mid]}: search left`,comment:`// Target is smaller than mid, so discard the right half and set high=${mid-1}.`});
      high=mid-1;
    } else {
      steps.push({arr,key,low,high,index:mid,nextLow:mid+1,nextHigh:high,decision:`${key} > ${arr[mid]}: search right`,comment:`// Target is larger than mid, so discard the left half and set low=${mid+1}.`});
      low=mid+1;
    }
  }
  steps.push({arr,key,low,high,index:-1,decision:`low(${low}) > high(${high}): NOT FOUND`,comment:'// Low crossed high, so the search interval is empty and the key is absent.'});
  return steps;
}
function renderSearchViz(){
  const display=document.getElementById('search-display'), body=document.getElementById('search-steps'), comment=document.getElementById('search-comment');
  if(!display || !body || !comment) return;
  const step=searchVizState.steps[searchVizState.index];
  if(!step){ display.innerHTML=''; body.innerHTML=''; comment.textContent='// Choose linear or binary search, then press Start.'; return; }
  display.innerHTML=step.arr.map((v,i)=>{
    const cls=[];
    if(i>=step.low && i<=step.high) cls.push('range'); else cls.push('eliminated');
    if(step.scanned && step.scanned.includes(i)) cls.push('eliminated');
    if(i===step.index) cls.push('active');
    if(i===step.found) cls.push('found');
    return `<div class="array-cell ${cls.join(' ')}">${vizEscape(v)}<div class="step-muted">${i}</div></div>`;
  }).join('');
  comment.textContent=step.comment;
  body.innerHTML=searchVizState.steps.slice(0,searchVizState.index+1).map((s,i)=>`<tr class="${i===searchVizState.index?'current-step':''}"><td>${i+1}</td><td>${s.low ?? '—'}</td><td>${s.high ?? '—'}</td><td>${s.index>=0?s.index:'—'}</td><td>${vizEscape(s.decision)}</td><td class="step-comment">${vizEscape(s.comment)}</td></tr>`).join('');
  body.lastElementChild?.scrollIntoView({block:'nearest'});
}
function startSearchViz(){
  clearTimeout(searchVizState.timer);
  const arr=parseVizNumbers('search-input'), key=parseInt(document.getElementById('search-key')?.value,10);
  if(!arr.length || !Number.isFinite(key)) return;
  searchVizState.steps=buildSearchSteps(searchVizState.algo,arr,key);
  searchVizState.index=0;
  renderSearchViz();
}
function stepSearchViz(){
  clearTimeout(searchVizState.timer);
  if(!searchVizState.steps.length){ startSearchViz(); return; }
  if(searchVizState.index<searchVizState.steps.length-1) searchVizState.index++;
  renderSearchViz();
}
function runSearchViz(){
  if(!searchVizState.steps.length) startSearchViz();
  clearTimeout(searchVizState.timer);
  const tick=()=>{
    if(searchVizState.index<searchVizState.steps.length-1){
      searchVizState.index++;
      renderSearchViz();
      searchVizState.timer=setTimeout(tick,620);
    }
  };
  tick();
}
function resetSearchViz(){
  clearTimeout(searchVizState.timer);
  searchVizState.steps=[]; searchVizState.index=-1;
  renderSearchViz();
}

function initAdvancedVisualizers(){
  resetSortViz();
  resetTreeViz();
  resetBstViz();
  resetExpressionViz();
  resetSearchViz();
}
initAdvancedVisualizers();
"""


def replace_between(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    if start_marker not in text:
        return text
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    return text[:start] + replacement + text[end:]


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")

    if "ADVANCED VISUALIZER LAYOUTS" not in text:
        text = text.replace("/* ── MISC ── */", ADVANCED_CSS + "\n/* ── MISC ── */")
    elif ".array-cell.active,.array-cell.found{opacity:1}" not in text:
        text = text.replace(
            ".array-cell.eliminated{opacity:.35}",
            ".array-cell.eliminated{opacity:.35}\n.array-cell.active,.array-cell.found{opacity:1}",
        )

    text = replace_between(
        text,
        "        <!-- Tree traversal visualizer -->",
        "      </div>\n    </div><!-- /ch6 -->",
        TREE_VISUALIZERS,
    )

    text = replace_between(
        text,
        "    <!-- ═══════ CH 8: SORTING",
        "    <!-- ═══════ CH 9: SEARCHING",
        CH8,
    )

    text = replace_between(
        text,
        "    <!-- ═══════ CH 9: SEARCHING",
        "  </div><!-- /content -->",
        CH9,
    )

    if "ADVANCED VISUALIZERS ADDED FROM THE PDF NOTES" not in text:
        text = text.replace("</script>\n</body>", ADVANCED_JS + "\n</script>\n</body>")

    TARGET.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
