/*!
 * ZwNetwork Library
 * https://github.com/OpenZWave/python-openzwave
 *
 * Copyright 2015 Sébastien GALLET aka bibi21000 <bibi21000@gmail.com>
 * Released under the GPL v3 license
 *
 * Date: 2015-04-14
 *
 */
(function() {
})();

function GetElementInsideContainer(containerID, childID) {
    var elm = document.getElementById(childID);
    var parent = elm ? elm.parentNode : {};
    return (parent.id && parent.id === containerID) ? elm : {};
}

// First, checks if it isn't implemented yet.
if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

