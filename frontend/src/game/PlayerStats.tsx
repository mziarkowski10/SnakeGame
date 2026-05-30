export default function PlayerStats() {
  return (
    <table>
      <tbody>
        <tr>
          <th>Score</th>
          <td id="score-value">0</td>
        </tr>
        <tr>
          <th>Length</th>
          <td id="length-value">3</td>
        </tr>
        <tr>
          <th>Direction</th>
          <td id="direction-value">RIGHT</td>
        </tr>
        <tr>
          <th>Status</th>
          <td id="status-value">Press arrow key to start</td>
        </tr>
      </tbody>
    </table>
  );
}
