"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * Convert from Vega-Lite to ASP.
 */
function vl2asp(spec) {
    const facts = [`mark(${spec.mark}).`];
    if ('data' in spec && 'url' in spec.data) {
        facts.push(`data("${spec.data.url}").`);
    }
    const encoding = spec.encoding || {};
    let i = 0;
    for (const channel of Object.keys(encoding)) {
        const eid = `e${i++}`;
        facts.push(`encoding(${eid}).`);
        facts.push(`channel(${eid},${channel}).`);
        let encFieldType = null;
        let encZero = null;
        let encBinned = null;
        // translate encodings
        for (const field of Object.keys(encoding[channel])) {
            const fieldContent = encoding[channel][field];
            if (field === 'type') {
                encFieldType = fieldContent;
            }
            if (field === 'bin') {
                encBinned = fieldContent;
            }
            if (field === 'scale') {
                // translate two boolean fields
                if ('zero' in fieldContent) {
                    encZero = fieldContent.zero;
                    if (fieldContent.zero) {
                        facts.push(`zero(${eid}).`);
                    }
                    else {
                        facts.push(`:- zero(${eid}).`);
                    }
                }
                if ('log' in fieldContent) {
                    if (fieldContent.log) {
                        facts.push(`log(${eid}).`);
                    }
                    else {
                        facts.push(`:-log(${eid}).`);
                    }
                }
            }
            else if (field === 'bin') {
                if (fieldContent.maxbins) {
                    facts.push(`${field}(${eid},${fieldContent.maxbins}).`);
                }
                else {
                    facts.push(`${field}(${eid},10).`);
                }
            }
            else if (field === 'field') {
                // fields can have spaces and start with capital letters
                facts.push(`${field}(${eid},"${fieldContent}").`);
            }
            else {
                // translate normal fields
                if (field !== 'bin') {
                    facts.push(`${field}(${eid},${fieldContent}).`);
                }
            }
        }
        if (encFieldType === 'quantitative' && encZero === null && encBinned === null) {
            facts.push(`zero(${eid}).`);
        }
    }
    return facts;
}
exports.default = vl2asp;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidmwyYXNwLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsiLi4vc3JjL3ZsMmFzcC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOztBQUVBOztHQUVHO0FBQ0gsU0FBd0IsTUFBTSxDQUFDLElBQTZCO0lBQzFELE1BQU0sS0FBSyxHQUFHLENBQUMsUUFBUSxJQUFJLENBQUMsSUFBSSxJQUFJLENBQUMsQ0FBQztJQUV0QyxJQUFJLE1BQU0sSUFBSSxJQUFJLElBQUksS0FBSyxJQUFJLElBQUksQ0FBQyxJQUFJLEVBQUU7UUFDeEMsS0FBSyxDQUFDLElBQUksQ0FBQyxTQUFTLElBQUksQ0FBQyxJQUFJLENBQUMsR0FBRyxLQUFLLENBQUMsQ0FBQztLQUN6QztJQUVELE1BQU0sUUFBUSxHQUFHLElBQUksQ0FBQyxRQUFRLElBQUksRUFBRSxDQUFDO0lBRXJDLElBQUksQ0FBQyxHQUFHLENBQUMsQ0FBQztJQUNWLEtBQUssTUFBTSxPQUFPLElBQUksTUFBTSxDQUFDLElBQUksQ0FBQyxRQUFRLENBQUMsRUFBRTtRQUMzQyxNQUFNLEdBQUcsR0FBRyxJQUFJLENBQUMsRUFBRSxFQUFFLENBQUM7UUFDdEIsS0FBSyxDQUFDLElBQUksQ0FBQyxZQUFZLEdBQUcsSUFBSSxDQUFDLENBQUM7UUFDaEMsS0FBSyxDQUFDLElBQUksQ0FBQyxXQUFXLEdBQUcsSUFBSSxPQUFPLElBQUksQ0FBQyxDQUFDO1FBRTFDLElBQUksWUFBWSxHQUFHLElBQUksQ0FBQztRQUN4QixJQUFJLE9BQU8sR0FBRyxJQUFJLENBQUM7UUFDbkIsSUFBSSxTQUFTLEdBQUcsSUFBSSxDQUFDO1FBRXJCLHNCQUFzQjtRQUN0QixLQUFLLE1BQU0sS0FBSyxJQUFJLE1BQU0sQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFDLE9BQU8sQ0FBQyxDQUFDLEVBQUU7WUFDbEQsTUFBTSxZQUFZLEdBQUcsUUFBUSxDQUFDLE9BQU8sQ0FBQyxDQUFDLEtBQUssQ0FBQyxDQUFDO1lBQzlDLElBQUksS0FBSyxLQUFLLE1BQU0sRUFBRTtnQkFDcEIsWUFBWSxHQUFHLFlBQVksQ0FBQzthQUM3QjtZQUNELElBQUksS0FBSyxLQUFLLEtBQUssRUFBRTtnQkFDbkIsU0FBUyxHQUFHLFlBQVksQ0FBQzthQUMxQjtZQUNELElBQUksS0FBSyxLQUFLLE9BQU8sRUFBRTtnQkFDckIsK0JBQStCO2dCQUMvQixJQUFJLE1BQU0sSUFBSSxZQUFZLEVBQUU7b0JBQzFCLE9BQU8sR0FBRyxZQUFZLENBQUMsSUFBSSxDQUFDO29CQUM1QixJQUFJLFlBQVksQ0FBQyxJQUFJLEVBQUU7d0JBQ3JCLEtBQUssQ0FBQyxJQUFJLENBQUMsUUFBUSxHQUFHLElBQUksQ0FBQyxDQUFDO3FCQUM3Qjt5QkFBTTt3QkFDTCxLQUFLLENBQUMsSUFBSSxDQUFDLFdBQVcsR0FBRyxJQUFJLENBQUMsQ0FBQztxQkFDaEM7aUJBQ0Y7Z0JBQ0QsSUFBSSxLQUFLLElBQUksWUFBWSxFQUFFO29CQUN6QixJQUFJLFlBQVksQ0FBQyxHQUFHLEVBQUU7d0JBQ3BCLEtBQUssQ0FBQyxJQUFJLENBQUMsT0FBTyxHQUFHLElBQUksQ0FBQyxDQUFDO3FCQUM1Qjt5QkFBTTt3QkFDTCxLQUFLLENBQUMsSUFBSSxDQUFDLFNBQVMsR0FBRyxJQUFJLENBQUMsQ0FBQztxQkFDOUI7aUJBQ0Y7YUFDRjtpQkFBTSxJQUFJLEtBQUssS0FBSyxLQUFLLEVBQUU7Z0JBQzFCLElBQUksWUFBWSxDQUFDLE9BQU8sRUFBRTtvQkFDeEIsS0FBSyxDQUFDLElBQUksQ0FBQyxHQUFHLEtBQUssSUFBSSxHQUFHLElBQUksWUFBWSxDQUFDLE9BQU8sSUFBSSxDQUFDLENBQUM7aUJBQ3pEO3FCQUFNO29CQUNMLEtBQUssQ0FBQyxJQUFJLENBQUMsR0FBRyxLQUFLLElBQUksR0FBRyxPQUFPLENBQUMsQ0FBQztpQkFDcEM7YUFDRjtpQkFBTSxJQUFJLEtBQUssS0FBSyxPQUFPLEVBQUU7Z0JBQzVCLHdEQUF3RDtnQkFDeEQsS0FBSyxDQUFDLElBQUksQ0FBQyxHQUFHLEtBQUssSUFBSSxHQUFHLEtBQUssWUFBWSxLQUFLLENBQUMsQ0FBQzthQUNuRDtpQkFBTTtnQkFDTCwwQkFBMEI7Z0JBQzFCLElBQUksS0FBSyxLQUFLLEtBQUssRUFBRTtvQkFDbkIsS0FBSyxDQUFDLElBQUksQ0FBQyxHQUFHLEtBQUssSUFBSSxHQUFHLElBQUksWUFBWSxJQUFJLENBQUMsQ0FBQztpQkFDakQ7YUFDRjtTQUNGO1FBRUQsSUFBSSxZQUFZLEtBQUssY0FBYyxJQUFJLE9BQU8sS0FBSyxJQUFJLElBQUksU0FBUyxLQUFLLElBQUksRUFBRTtZQUM3RSxLQUFLLENBQUMsSUFBSSxDQUFDLFFBQVEsR0FBRyxJQUFJLENBQUMsQ0FBQztTQUM3QjtLQUNGO0lBRUQsT0FBTyxLQUFLLENBQUM7QUFDZixDQUFDO0FBcEVELHlCQW9FQyJ9