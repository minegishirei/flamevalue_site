import { TweenMax } from 'gsap';

/**
 * TweenMax の基本操作
 */
export default class TweenAnimation {
  /**
   * @param {any} target
   * @param {number} duration
   * @param {gsap.TweenConfig} vars
   */
  constructor(target, duration, vars) {
    this._tween = TweenMax.to(target, duration, vars);
  }

  /**
   * アニメーションを止める
   * @param {any} [atTime]
   * @param {boolean} [suppressEvents]
   */
  pause(atTime, suppressEvents) {
    this._tween.pause(atTime, suppressEvents);
  }
}