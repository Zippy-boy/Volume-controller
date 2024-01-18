<script lang="ts">
  import * as tasklist from 'tasklist';

  let appList = tasklist(function(err, tasks) {
    if (err) throw err; // TODO: proper error handling
      tasks.filter(function(task) {
      return task.imageName.indexOf('ll_') === 0;
    }).map(function(task) {
      return {
        id   : task.pid, // XXX: is that the same as your `id`?
        name : task.imageName,
      };
    });
  });

</script>

<div class="wrapper">
  <div class="top"></div>
  <div class="bottom">
    <ul>
      {#each appList as app}
        <li>{app.name}</li>
      {/each}
    </ul>
  </div>
</div>
<style>
  .wrapper {
    display: flex;
    flex-direction: column;
    /* align-items: center; */
    /* justify-content: center; */
    height: 100%;
    color: #c2f5ff;
  }

  .top, .bottom {
    background-color: #404653;
    height: 50%;
    border: #404653 solid 4px;
    width: 100px;
    border-radius: 20px;
  }


  .versions {
    margin: 0 auto;
    float: none;
    clear: both;
    overflow: hidden;
    font-family: 'Menlo', 'Lucida Console', monospace;
    color: #c2f5ff;
    line-height: 1;
    transition: all 0.3s;
  }

  .versions li {
    display: block;
    float: left;
    border-right: 1px solid rgba(194, 245, 255, 0.4);
    padding: 0 20px;
    font-size: 13px;
    opacity: 0.8;
  }

  .versions li:last-child {
    border: none;
  }

  @media (max-width: 840px) {
    .versions {
      display: none;
    }
  }
</style>
