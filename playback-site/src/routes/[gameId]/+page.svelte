<script lang="ts">
  import Player from "./Player.svelte";

  const { data } = $props();
</script>

<div class="page-container">
  <section class="pitch">
    <div class="field left">
      <div class="penalty-area"></div>
    </div>
    <div class="field right">
      <div class="penalty-area"></div>
    </div>
    <div class="center-circle"></div>
    {#await data.data then data}
      <Player gameData={data} />
    {/await}
  </section>
</div>

<style>
  .page-container {
    display: flex;
    height: 100vh;
    width: 100%;
    /* align-items: center;
    justify-content: center; */
  }

  .pitch {
    background-color: #238729;
    width: 590px;
    height: 380px;
    position: relative;
  }
  .pitch:after {
    content: "";
    border-left: 1px solid white;
    position: absolute;
    top: 20px;
    left: 295px;
    display: block;
    height: 340px;
  }

  .pitch:before {
    content: "";
    border: 1px solid white;
    position: absolute;
    top: 20px;
    left: 20px;
    display: block;
    width: 550px;
    height: 340px;
  }

  .center-circle {
    position: absolute;
    top: 145px;
    left: 250px;
    width: 90px;
    height: 90px;
    border: 1px solid white;
    border-radius: 50%;
  }
  .center-circle:after {
    position: absolute;
    top: 43px;
    left: 43px;
    width: 1px;
    height: 1px;
    background-color: white;
    content: "";
    border: 1px solid white;
  }

  .penalty-area {
    position: absolute;
    height: 140px;
    width: 80px;
    top: 120px;
    border: 1px solid white;
  }

  .left .penalty-area {
    left: 20px;
    border-left: 0;
  }

  .right .penalty-area {
    right: 19px;
    border-right: 0;
  }

  .penalty-area:before {
    position: absolute;
    height: 70px;
    width: 35px;
    top: 35px;
    border: 1px solid white;
    content: "";
  }
  .left .penalty-area:before {
    left: 0px;
    border-left: 0;
  }
  .right .penalty-area:before {
    right: 0px;
    border-right: 0;
  }

  .penalty-area:after {
    position: absolute;
    height: 2px;
    width: 2px;
    top: 70px;
    background-color: white;
    content: "";
  }
  .left .penalty-area:after {
    right: 15px;
  }
  .right .penalty-area:after {
    left: 15px;
  }
</style>
