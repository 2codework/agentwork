# 已知合成片段时间表（不是ASR转录）

时间是实际拼接PCM的样本边界，含flite片段自身短停顿；SRT为句级近似区间，不是逐词对齐。三事实不可删；全文见script.en.txt。

|句号（0起）|区段|开始秒|结束秒|完整送入合成器的句子|
|---|---|---:|---:|---|
|0|Opening|0.000000|8.377812|Here is a simple way to compare two paper-plane designs without turning a small experiment into a confusing guessing game.|
|1|Opening|8.557813|12.650458|We are not trying to prove which plane is best for everyone.|
|2|Opening|12.830458|18.877229|We are only comparing our two designs under the same conditions in one practice session.|
|3|Fact F1|19.057229|24.959396|In this practice test, both planes use one sheet of the same size and type of paper.|
|4|Fact F1|25.139396|28.072187|Only the fold design changes.|
|5|Extra explanation|28.252188|30.810000|You can name the designs A and B.|
|6|Extra explanation|30.990000|35.362792|Write the names on a separate record sheet, not on the planes.|
|7|Extra explanation|35.542792|40.402771|Clear a safe indoor space and keep people out of the flight path.|
|8|Extra explanation|40.582771|44.280437|Use the same starting line for every throw.|
|9|Fact F2|44.460437|50.349729|Each design gets three throws, so this practice session has six throws in total.|
|10|Extra explanation|50.529729|55.393708|Take turns between A and B rather than finishing one design first.|
|11|Extra explanation|55.573708|60.027833|This is a small practice exercise, not a competition.|
|12|Extra explanation|60.207833|67.583708|A surprising result is still worth writing down, and one long flight does not tell the whole story.|
|13|Fact F3|67.763708|72.113542|Record all six distances, including short flights.|
|14|Fact F3|72.293542|76.838958|Do not discard a result just because it looks disappointing.|
|15|Ending|77.018958|80.104708|Keep the record with the two design names.|
|16|Ending|80.284708|87.335542|Now another person can see what you actually measured, rather than only hearing which plane you liked.|
