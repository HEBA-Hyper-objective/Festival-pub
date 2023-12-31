import React from "react";
import "styles/AlarmModal.scss";
import ExitTimeImg from "assets/images/Timeout.svg";
import CloseBtn from "assets/images/alarmClose.svg";

const ExitTimeAlarm = ({onClose, time}) => {
  return (
    <div className="leftTimeAlarmBox">
      <div className="leftTimeImg">
        <img src={ExitTimeImg} alt="alarm img"></img>
      </div>
      <div className="lefTimeMessage">
        <span className="alarmSpanMiddle" style={{color: '#e40049', fontWeight:'700'}}>
          퇴장 시간을 초과하였습니다.
        </span>
        <span className="alarmSpanSmall">
	  { time }
        </span>
      </div>
      <div className="alarmCloseBtn" onClick={onClose}>
        <img src={CloseBtn} alt="close img"></img>
      </div>
    </div>
  );
}

export default ExitTimeAlarm;
